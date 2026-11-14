"""
benchmark.py — Multi-threaded CPU & GPU Micro-benchmarking
Measures multi-core floating point throughput and evaluates GPU compute tiers.
"""

import time
from concurrent.futures import ThreadPoolExecutor

def _cpu_worker(n):
    total = 0.0
    for i in range(n):
        total += (i * 0.0001) ** 2
    return total

def benchmark_cpu(cores_logical=4):
    ops_per_thread = 2_000_000
    threads = max(1, cores_logical)
    
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(_cpu_worker, ops_per_thread) for _ in range(threads)]
        for f in futures:
            f.result()
    t1 = time.perf_counter()
    elapsed = max(0.001, t1 - t0)
    
    total_ops = ops_per_thread * threads
    mflops = (total_ops / elapsed) / 1_000_000.0
    
    # Modern reference CPU (e.g. Ryzen 7 7800X3D or i7-14700) scores ~80-120 MFLOPS in this test.
    # Older quad-cores (i7-4790, i5-6400) score ~3-10 MFLOPS.
    score = round(min(100.0, max(5.0, (mflops / 80.0) * 100.0)), 1)
    return score, round(mflops, 1), round(elapsed * 1000, 1)

def evaluate_gpu_tier(gpu_info):
    if not gpu_info["devices"]:
        return 5.0, "No Dedicated GPU Found"

    name = gpu_info["devices"][0]["name"].lower()
    
    if any(k in name for k in ["4090", "4080", "3090", "3080", "7900"]):
        score = 100.0
        tier = "Ultra Enthusiast (DirectML/CUDA/Vulkan)"
    elif any(k in name for k in ["6600", "6700", "3060", "3070", "4060", "7600", "a770"]):
        score = 85.0
        tier = "Mid-Range Dedicated (DirectML/ROCm/CUDA)"
    elif any(k in name for k in ["1660", "1070", "1080", "2060", "580", "590", "3050", "6500"]):
        score = 60.0
        tier = "Entry-Level Dedicated"
    elif any(k in name for k in ["1050", "960", "750", "550"]):
        score = 35.0
        tier = "Legacy Dedicated"
    else:
        score = 25.0
        tier = "Integrated / Generic Graphics"

    return score, tier
