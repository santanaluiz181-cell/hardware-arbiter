"""
cli.py — Hardware Arbiter Command Line Interface
Presents hardware scores, diagnostic tables, and applies workload governor policies.
"""

import sys
import json
import argparse

from .governor import evaluate_and_govern
from .i18n import t
from mascot.paint_mascot_ascii import get_mascot_banner

def main():
    parser = argparse.ArgumentParser(
        description="Hardware Arbiter — Autonomous Hardware Profiler & Bottleneck Governor"
    )
    parser.add_argument("--apply", action="store_true", help="Apply thread limits and governor policies to system environment")
    parser.add_argument("--lang", choices=["en", "pt", "zh"], default="en", help="Interface language (en: English, pt: Português, zh: 中文)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON structure")
    parser.add_argument("--benchmark-only", action="store_true", help="Run benchmark without saving profile")

    args = parser.parse_args()

    result = evaluate_and_govern(apply_tuning=args.apply, lang=args.lang)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    # Print ASCII mascot banner
    banner = get_mascot_banner(profile=result["profile"], hri=result["hri"], lang=args.lang)
    print(banner)

    # Summary Card
    hw = result["hardware"]
    scores = result["scores"]
    print("=" * 70)
    print(f"  {t('cpu_detected', args.lang)}: {hw['cpu']} ({hw['cores']})")
    print(f"  {t('cpu_score', args.lang)}: {scores['cpu_score']}/100 ({scores['cpu_mflops']} MFLOPS)")
    print("-" * 70)
    print(f"  {t('gpu_detected', args.lang)}: {hw['gpu']} (VRAM: {hw['vram_gb']} GB)")
    print(f"  {t('gpu_score', args.lang)}: {scores['gpu_score']}/100 [{scores['gpu_tier']}]")
    print("=" * 70)
    print(f"  >> {t('hri_label', args.lang)}: {result['hri']}x")
    print(f"  >> {t('profile_label', args.lang)}: [{result['profile']}]")
    print("=" * 70)
    print(f"\n[DIAGNOSIS]\n{result['diagnosis']}\n")

    # Allocation Table
    print(f"{t('table_component', args.lang):<32} | {t('table_state', args.lang)}")
    print("-" * 70)
    pol = result["policies"]
    print(f"{t('embeddings', args.lang):<32} | {pol['vector_embeddings']}")
    print(f"{t('vision_ocr', args.lang):<32} | {pol['vision_ocr']}")
    print(f"{t('transcription', args.lang):<32} | {pol['transcription_asr']}")
    print(f"{t('electron_render', args.lang):<32} | {pol['electron_hardware_acceleration']}")
    print(f"{t('priority', args.lang):<32} | {pol['subagent_priority']}")
    
    threads = ", ".join(f"{k}={v}" for k, v in pol["thread_limits"].items())
    print(f"{t('thread_limits', args.lang):<32} | {threads}")
    print("-" * 70)

    if args.apply:
        print(f"\n[OK] {t('policies_applied', args.lang)}")
        print(f"[OK] {t('thread_clamp_applied', args.lang)}")
    else:
        print(f"\nTip: Run with --apply to enforce these thread clamps and protect your CPU.")

    print(f"\n{t('cache_recommendation', args.lang)}\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
