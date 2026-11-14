---
name: hardware-arbiter
description: Perfilador autônomo de hardware e governador dinâmico de carga computacional (CPU vs GPU) para Antigravity. Diagnostica gargalos, calcula o Hardware Ratio Index (HRI) e aloca tarefas locais automaticamente (DirectML, Vulkan, thread clamping).
---

# Hardware Arbiter (Governador de Gargalo e Descarregamento de Carga)

A skill **Hardware Arbiter** permite que qualquer instância do Antigravity identifique automaticamente a assimetria entre o processador (CPU) e a placa de vídeo (GPU) da máquina hospedeira, calcule o **Hardware Ratio Index (HRI)** e equilibre dinamicamente as tarefas locais para poupar o componente mais fraco e sobrecarregar o mais forte.

---

## 1. Princípio de Funcionamento (Hardware Ratio Index - HRI)

O Hardware Arbiter executa um micro-benchmark determinístico de multi-threading FP32 e memória na CPU e audita a arquitetura, VRAM e provedores da GPU (DirectML, Vulkan, CUDA, ROCm, Metal).

A métrica central é o **Hardware Ratio Index (HRI)**:
$$HRI = \frac{Score_{GPU}}{Score_{CPU}}$$

### Perfis de Operação:
1. **`GPU_DOMINANT` ($HRI \ge 2.0$):**
   - **Cenário:** CPU antiga ou fraca (ex: Core i7 de 4ª geração, i3, Celeron, Ryzen 3) combinada com GPU moderna (ex: RX 6600, RTX 3060/4060).
   - **Ação:** Delega 100% de embeddings vetoriais, OCR, visão, ASR e renderização para a GPU via DirectML/Vulkan.
   - **Proteção da CPU:** Aplica *Thread Clamping* (`OMP_NUM_THREADS=2`, `MKL_NUM_THREADS=2`, `UV_THREADPOOL_SIZE=4`) para impedir que bibliotecas tentem usar todos os threads da CPU e travem o editor. Subprocessos rodam em prioridade `BelowNormal`.
2. **`BALANCED` ($0.6 < HRI < 2.0$):**
   - **Cenário:** CPU e GPU equilibradas (ex: Ryzen 5 5600 + RTX 3060).
   - **Ação:** Divisão híbrida 50/50. Tarefas vetoriais na GPU, I/O e pipelines locais em paralelo com threads normais.
3. **`CPU_DOMINANT` ($HRI \le 0.6$):**
   - **Cenário:** Processador muito forte (ex: Ryzen 9, Core i9, Xeon) com GPU integrada básica (Intel UHD/AMD Radeon Graphics) ou sem VRAM dedicada.
   - **Ação:** Prioriza instruções vetoriais AVX2/AVX-512 na CPU para inferências locais (OpenVINO, XNNPACK) e poupa a GPU fraca apenas para exibição da interface.

---

## 2. Como Usar

### Diagnóstico de Gargalo (Apenas Leitura):
```bash
python -m hardware_arbiter.cli
```

### Aplicar Otimizações Automaticamente no Sistema:
```bash
python -m hardware_arbiter.cli --apply
```
O parâmetro `--apply`:
- Injeta os limites de threads de CPU no escopo `User` do Windows (ou variáveis de sessão no Linux/macOS).
- Atualiza o `settings.json` do Antigravity (`terminal.integrated.env.windows`).
- Gera o manifesto de estado em `~/.hardware_arbiter_profile.json`.

### Suporte a Idiomas:
```bash
python -m hardware_arbiter.cli --lang pt   # Português
python -m hardware_arbiter.cli --lang zh   # 中文
python -m hardware_arbiter.cli --lang en   # English
```
