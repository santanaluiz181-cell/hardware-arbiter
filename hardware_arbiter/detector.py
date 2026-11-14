"""
detector.py — Cross-platform CPU & GPU Hardware Detection
Discovers physical/logical cores, GPU models, VRAM, and runtime providers.
Supports Windows, Linux, and macOS.
"""

import os
import sys
import json
import platform
import subprocess

def detect_cpu():
    info = {
        "model": platform.processor() or "Unknown CPU",
        "cores_logical": os.cpu_count() or 4,
        "cores_physical": os.cpu_count() or 4,
        "arch": platform.machine(),
        "platform": sys.platform
    }
    
    if sys.platform == "win32":
        try:
            cmd = "Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors | ConvertTo-Json"
            res = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                if isinstance(data, list):
                    data = data[0]
                info["model"] = data.get("Name", info["model"]).strip()
                info["cores_physical"] = data.get("NumberOfCores", info["cores_physical"])
                info["cores_logical"] = data.get("NumberOfLogicalProcessors", info["cores_logical"])
        except Exception:
            pass
    elif sys.platform == "linux":
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
                for line in f:
                    if "model name" in line:
                        info["model"] = line.split(":", 1)[1].strip()
                        break
        except Exception:
            pass
    elif sys.platform == "darwin":
        try:
            res = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True, timeout=3)
            if res.returncode == 0:
                info["model"] = res.stdout.strip()
        except Exception:
            pass
            
    return info

def detect_gpu():
    gpus = []
    
    if sys.platform == "win32":
        try:
            cmd = "Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion | ConvertTo-Json"
            res = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    name = item.get("Name", "")
                    if "virtual" in name.lower() or "basic render" in name.lower():
                        continue
                    vram_bytes = item.get("AdapterRAM", 0) or 0
                    vram_gb = round(vram_bytes / (1024**3), 2)
                    gpus.append({
                        "name": name,
                        "vram_gb": vram_gb,
                        "driver": item.get("DriverVersion", "")
                    })
        except Exception:
            pass
    elif sys.platform == "linux":
        try:
            res = subprocess.run(["lspci"], capture_output=True, text=True, timeout=3)
            for line in res.stdout.splitlines():
                if "VGA" in line or "3D" in line:
                    gpus.append({"name": line.split(":", 2)[-1].strip(), "vram_gb": 0, "driver": "Linux DRM"})
        except Exception:
            pass
    elif sys.platform == "darwin":
        gpus.append({"name": "Apple Silicon Unified GPU", "vram_gb": 0, "driver": "Metal"})

    # Check ONNX / Tensor execution providers
    providers = []
    dml_active = False
    cuda_active = False
    try:
        import onnxruntime as ort
        providers = ort.get_available_providers()
        dml_active = "DmlExecutionProvider" in providers
        cuda_active = "CUDAExecutionProvider" in providers
    except Exception:
        pass

    return {
        "devices": gpus,
        "onnx_providers": providers,
        "directml_available": dml_active,
        "cuda_available": cuda_active
    }
