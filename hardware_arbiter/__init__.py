"""
Hardware Arbiter — Autonomous Hardware Profiler & Workload Governor
"""

__version__ = "0.1.0"
__author__ = "Santana Luiz"

from .governor import evaluate_and_govern
from .detector import detect_cpu, detect_gpu
from .benchmark import benchmark_cpu, evaluate_gpu_tier

__all__ = [
    "evaluate_and_govern",
    "detect_cpu",
    "detect_gpu",
    "benchmark_cpu",
    "evaluate_gpu_tier",
]
