"""
governor.py — Hardware Ratio Index (HRI) & Dynamic Workload Governor
Decides the optimal compute strategy and applies environment and thread clamps.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

from .detector import detect_cpu, detect_gpu
from .benchmark import benchmark_cpu, evaluate_gpu_tier
from .i18n import t

def evaluate_and_govern(apply_tuning=False, lang="en"):
    cpu = detect_cpu()
    gpu = detect_gpu()
    
    cpu_score, cpu_mflops, cpu_elapsed = benchmark_cpu(cpu["cores_logical"])
    gpu_score, gpu_tier = evaluate_gpu_tier(gpu)

    # Hardware Ratio Index (HRI)
    hri = round(gpu_score / (cpu_score + 1e-6), 2)

    if hri >= 2.0:
        profile = "GPU_DOMINANT"
        diagnosis = t("diagnosis_gpu_dominant", lang)
    elif hri <= 0.6:
        profile = "CPU_DOMINANT"
        diagnosis = t("diagnosis_cpu_dominant", lang)
    else:
        profile = "BALANCED"
        diagnosis = t("diagnosis_balanced", lang)

    clamp_threads = "2" if profile == "GPU_DOMINANT" else str(max(2, cpu["cores_logical"] - 1))
    
    result = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "profile": profile,
        "hri": hri,
        "scores": {
            "cpu_score": cpu_score,
            "cpu_mflops": cpu_mflops,
            "gpu_score": gpu_score,
            "gpu_tier": gpu_tier
        },
        "hardware": {
            "cpu": cpu["model"],
            "cores": f"{cpu['cores_physical']}C / {cpu['cores_logical']}T",
            "gpu": gpu["devices"][0]["name"] if gpu["devices"] else "N/A",
            "vram_gb": gpu["devices"][0]["vram_gb"] if gpu["devices"] else 0,
            "directml": gpu["directml_available"],
            "cuda": gpu["cuda_available"]
        },
        "diagnosis": diagnosis,
        "policies": {
            "vector_embeddings": "GPU (DirectML / CUDA)" if profile != "CPU_DOMINANT" else "CPU (AVX2)",
            "vision_ocr": "GPU (DirectML)" if profile != "CPU_DOMINANT" else "CPU",
            "transcription_asr": "GPU (Vulkan / AMF)" if profile != "CPU_DOMINANT" else "CPU (AVX2)",
            "electron_hardware_acceleration": "ENABLED (Forced Desktop GL & Rasterization)",
            "thread_limits": {
                "OMP_NUM_THREADS": clamp_threads,
                "MKL_NUM_THREADS": clamp_threads,
                "UV_THREADPOOL_SIZE": "4" if profile == "GPU_DOMINANT" else "8",
                "RAYON_NUM_THREADS": clamp_threads
            },
            "subagent_priority": "BelowNormal" if profile == "GPU_DOMINANT" else "Normal",
            "defender_cache_exclusion_recommended": True
        }
    }

    # Persist profile to disk for other tools/subagents to read
    profile_path = Path.home() / ".hardware_arbiter_profile.json"
    try:
        profile_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

    if apply_tuning and sys.platform == "win32":
        # Injeta limites de threads no registro do Windows (User env)
        for k, v in result["policies"]["thread_limits"].items():
            try:
                subprocess.run(
                    ["powershell", "-NoProfile", "-Command", f"[Environment]::SetEnvironmentVariable('{k}', '{v}', 'User')"],
                    check=False
                )
            except Exception:
                pass

        # Injeta variáveis no settings.json do Antigravity
        settings_paths = [
            Path(os.environ.get("APPDATA", "")) / "Antigravity" / "User" / "settings.json",
            Path(os.environ.get("APPDATA", "")) / "Antigravity IDE" / "User" / "settings.json"
        ]
        for p in settings_paths:
            if p.exists():
                try:
                    s_data = json.loads(p.read_text(encoding="utf-8"))
                    env_win = s_data.get("terminal.integrated.env.windows", {})
                    for k, v in result["policies"]["thread_limits"].items():
                        env_win[k] = v
                    s_data["terminal.integrated.env.windows"] = env_win
                    p.write_text(json.dumps(s_data, indent=4, ensure_ascii=False), encoding="utf-8")
                except Exception:
                    pass

    return result
