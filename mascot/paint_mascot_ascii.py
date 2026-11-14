"""
paint_mascot_ascii.py — ASCII Art & ANSI Banner of Paint the Arbiter
Renders Paint, the retro-style roller mascot, in pure terminal characters.
"""

def get_mascot_banner(profile="GPU_DOMINANT", hri=17.0, lang="en"):
    cyan = "\033[96m"
    amber = "\033[93m"
    green = "\033[92m"
    reset = "\033[0m"
    bold = "\033[1m"
    dim = "\033[2m"

    taglines = {
        "en": "Dynamic Workload Balancer & Bottleneck Governor",
        "pt": "Governador Dinâmico de Gargalo e Distribuição de Carga",
        "zh": "动态工作负载平衡器与硬件瓶颈调度器"
    }
    tag = taglines.get(lang, taglines["en"])

    banner = rf"""
{cyan}   ____  ___    _____   _________{reset}       {dim}.-._______________________.-.{reset}
{cyan}  / __ \/   |  /  _/ | / /_  __/{reset}       {dim}|{reset} {bold}PAINT THE ARBITER{reset}          {dim}|{reset}
{cyan} / /_/ / /| |  / //  |/ / / /   {reset}       {dim}|{reset} {cyan}GPU: DirectML / Vulkan{reset}    {dim}|{reset}
{cyan}/ ____/ ___ |_/ // /|  / / /    {reset}  <O>  {dim}|{reset} {amber}CPU: Thread-Clamped{reset}       {dim}|{reset}
{cyan}/_/   /_/  |_/___/_/ |_/ /_/     {reset}  /|\  {dim}'-'-----------------------'-'{reset}
                                   / \   {green}[HRI: {hri}x | {profile}]{reset}
{dim}:: {tag} ::{reset}
"""
    return banner
