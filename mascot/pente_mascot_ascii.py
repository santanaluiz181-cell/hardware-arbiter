"""
pente_mascot_ascii.py — ASCII Art & ANSI Banner of Pente Fino the Comb Mascot
Renders Pente Fino, the dapper hair comb mascot that separates GPU tasks from CPU tasks.
"""

def get_mascot_banner(profile="GPU_DOMINANT", hri=17.0, lang="en"):
    cyan = "\033[96m"
    amber = "\033[93m"
    green = "\033[92m"
    gold = "\033[33m"
    reset = "\033[0m"
    bold = "\033[1m"
    dim = "\033[2m"

    taglines = {
        "en": "Passando o Pente Fino: Combing heavy tasks to GPU, settling CPU clean",
        "pt": "Passando o Pente Fino: Cargas pesadas vão com a GPU, CPU fica leve",
        "zh": "精准硬件梳理器：重度张量随梳入GPU，底层轻量留驻CPU"
    }
    tag = taglines.get(lang, taglines["en"])

    banner = rf"""
{gold}          __             __{reset}
{gold}     .---'  '-----------'  '---.{reset}        {dim}.-._____________________________.-.{reset}
{gold}    /                           \{reset}       {dim}|{reset} {bold}PENTE FINO :: HARDWARE COMB{reset}    {dim}|{reset}
{gold}   (   (o)                 (O)-o ){reset}      {dim}|{reset} {cyan}GPU: Leva o peso com o pente{reset}   {dim}|{reset}
{gold}    \           <w>             /{reset}       {dim}|{reset} {amber}CPU: Raiz assentada e limpa{reset}    {dim}|{reset}
{gold}     '===|===|===|===|===|===|='{reset}        {dim}'-'----------------------------'-'{reset}
{cyan}         |   |   |   |   |   |{reset}   {green}[HRI: {hri}x | {profile}]{reset}
{cyan}         |   |   |   |   |   |{reset}
{cyan}         |   |   |   |   |   |{reset}   {cyan}~~~~~ GPU OFFLOAD (DirectML/Vulkan) ~~~~~>{reset}
{amber}        ( ) ( ) ( ) ( ) ( ) ( ){reset}  {amber}..... CPU ROOT (Thread-Clamped) .....{reset}

{dim}:: {tag} ::{reset}
"""
    return banner
