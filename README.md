# Hardware Arbiter 🪮⚖️

<p align="center">
  <img src="mascot/hero-banner.svg" alt="Hardware Arbiter Hero Banner — Passando o Pente Fino" width="100%" />
</p>

> **Passando o Pente Fino no Hardware:** O peso vai com os dentes do pente direto para a GPU; a CPU fica limpa, com os fios assentados e zero travamentos.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-38bdf8.svg)](https://www.python.org/)
[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Agent%20Skill-10b981.svg)](SKILL.md)
[![Accelerators](https://img.shields.io/badge/Backends-DirectML%20%7C%20CUDA%20%7C%20Vulkan-f59e0b.svg)]()
[![GitHub Pages](https://img.shields.io/badge/Showcase-Live%20Demo-0284c7.svg)](https://santanaluiz181-cell.github.io/hardware-arbiter/)

---

## 🪮 Conheça o "Pente" (The Hardware Comb Mascot)

O **Pente** é o mascote oficial do Hardware Arbiter. Ele é um animalzinho dapper e fofo que personifica a triagem de hardware do ecossistema, criado com a mesma dedicação artesanal da **Foquinha** (MJ Notch), da **Raposa Kitsune** (Kitsune Router) e do **Elefante Phanty** (Ultimate Research / DESLOP):

- **Anatomia & Animação Orgânica (SVG Vivo):**
  - **Silhueta de Loaf/Feijão Orgânica:** Curvas suaves em pera/feijão com flat base, sticker halo (`#111218`), máscara facial taupe (`#7E6C6A`), focinho creme e colete social azul-marinho (`#22445D`).
  - **Expressividade Real:** Respiração orgânica (`4.2s`), piscadas de olho periódicas com duplo brilho anime (`4.6s`), rastreamento de olhar por pupila, fungada de focinho com boca :3 e orelhas atentas que tremelicam.
  - **Ação Viva de Pentear:** Suas patinhas redondas passam o pente de âmbar com 8 dentes de precisão (`2.4s`), desembaraçando os tensores em tempo real.
- **Os Fios Passam Pela Frente (O Princípio Operacional):**
  - **Fios Elétricos Caóticos à Esquerda (CPU Bottleneck):** Os nós de tensores pesados (embeddings, OCR, visão, Whisper ASR) chegam como mechas neon ciano cheias de nós e partículas elétricas.
  - **Passagem Visível pela Frente do Corpo:** As mechas passam **visivelmente pela frente do peito e do colete do animalzinho**, entrando diretamente entre os dentes do pente de âmbar.
  - **Feixes de Laser Paralelos à Direita (GPU Offload):** Saindo dos dentes do pente, as mechas são alinhadas em 6 feixes de laser horizontais perfeitamente paralelos e sincronizados, descarregados na GPU (DirectML / CUDA / Vulkan).
  - **A Raiz Fica Limpa na CPU:** As rotinas leves de sistema (I/O, Git, terminal) permanecem assentadas na CPU, blindadas por **Thread Clamping (`OMP=2`, `UV=4`)** para o editor e o cursor nunca mais engasgarem.

<p align="center">
  <img src="mascot/pente_mascot.svg" alt="Mascote Pente — Penteando fios caóticos em feixes de laser GPU" width="700" />
</p>

---

## 🌐 Seleção de Idioma / Language Selector / 语言导航

- [Português 🇧🇷](#-português)
- [English 🇺🇸](#-english)
- [中文 🇨🇳](#-中文)

---

## 🇧🇷 Português

### A Dor Real de Engenharia
Você coloca uma GPU moderna no computador (como uma AMD RX 6600 ou RTX 3060), mas o seu processador é de 4 núcleos mais antigo (como um Core i7 Haswell de 2014). Quando ferramentas locais de IA ou agentes começam a rodar, bibliotecas como PyTorch ou ONNX tentam instanciar 8 a 16 threads de CPU simultaneamente. 

O resultado: **tempestade de troca de contexto (context-switching storm)**, mouse congelando e editor travado, enquanto a GPU com 8GB de VRAM fica parada com 4% de uso.

### Como o Hardware Arbiter Resolve
O script executa um micro-benchmark determinístico multi-thread, audita a GPU e calcula o **Índice de Razão de Hardware (HRI)**:

$$HRI = \frac{Score_{GPU}}{Score_{CPU}}$$

| Perfil | Faixa de HRI | Cenário de Hardware | Ação do Pente Fino |
| :--- | :--- | :--- | :--- |
| **`GPU_DOMINANT`** | $HRI \ge 2.0$ | CPU fraca/antiga + GPU Dedicada Forte (ex: i7-4790 + RX 6600) | **O pente puxa tudo:** 100% de embeddings vetoriais, visão e transcrição vão para a GPU via DirectML/Vulkan. Na CPU, aplica **Thread Clamping (`OMP=2`, `UV=4`)** e prioridade `BelowNormal` em subprocessos. |
| **`BALANCED`** | $0.6 < HRI < 2.0$ | Máquina equilibrada (ex: Ryzen 5 5600 + RTX 3060) | Divisão 50/50 simétrica. Matemática na GPU, pipelines de compilação e I/O com threads livres na CPU. |
| **`CPU_DOMINANT`** | $HRI \le 0.6$ | CPU potente + GPU integrada/básica (ex: i9 / Ryzen 9 + iGPU) | O pente deixa a matemática na CPU via AVX2/AVX-512, poupando a GPU fraca apenas para renderização de tela. |

### Instalação Rápida
```bash
# Clonar o repositório
git clone https://github.com/santanaluiz181-cell/hardware-arbiter.git
cd hardware-arbiter
pip install -e .

# Apenas diagnosticar o PC (leitura)
hardware-arbiter --lang pt

# Aplicar o pente fino e travar as variáveis no sistema
hardware-arbiter --apply --lang pt
```

---

## 🇺🇸 English

### The Problem
AI tools and coding agents often launch unconstrained worker threads (`OMP_NUM_THREADS`, `UV_THREADPOOL_SIZE`). When paired with an older quad-core CPU and a modern GPU, your CPU gets smothered by context switches while 8GB of high-speed GDDR6 VRAM sits idle.

### The Comb Solution
The **Dapper Comb (Pente Fino)** sweeps through your hardware:
- **Tensors, embeddings, OCR, and speech recognition** get caught in the comb teeth and channeled straight to the GPU.
- **Lightweight OS routines** stay comfortably at the roots on the CPU under strict thread clamping.

### CLI Usage
```bash
# Run trilingual diagnostic
hardware-arbiter --lang en

# Enforce thread clamps & policies
hardware-arbiter --apply --lang en
```

---

## 🇨🇳 中文

### 硬件细齿梳哲学
将系统负载如秀发般精准梳理：
- **重度张量计算**（向量嵌入、OCR视觉、Whisper语音转写）顺着梳齿彻底梳入独立 GPU（DirectML / CUDA / Vulkan）。
- **底层轻量例程**（文件I/O、终端、Git）如同健康发根安稳留驻在 CPU 端，辅以严格的线程钳制 (`OMP=2`, `UV=4`) 杜绝界面冻结。

### 运行方式
```bash
# 诊断当前机器算力比例
hardware-arbiter --lang zh

# 自动将优化配置写入系统环境
hardware-arbiter --apply --lang zh
```

---

## 📊 Live Interactive Showcase (GitHub Pages)

Acesse a demonstração interativa completa em [santanaluiz181-cell.github.io/hardware-arbiter](https://santanaluiz181-cell.github.io/hardware-arbiter/):
- Simulador interativo de HRI com seletor de CPU e GPU.
- Arte vetorial interativa do mascote Pente Fino.
- Design técnico 100% livre de clichês visuais de IA.

---

## 📜 Licença
Distribuído sob licença MIT • Autor: **Santana Luiz** (`santanaluiz181-cell`).
