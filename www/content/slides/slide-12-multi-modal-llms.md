+++
title = "Architecting Multi-modal LLMs"
description = "How to add vision, audio and other cognitive perceptions to AI agents"
weight = 120
outputs = ["Reveal"]
math = true
thumbnail = "/imgs/slides/multimodal_llm_slide_title.png"

[reveal_hugo]
custom_theme = "css/reveal-robinson.css"
slide_number = true
transition = "none"

+++

{{< slide background-image="/imgs/slides/multimodal_llm_slide_title.png" >}}
<div style="min-height: 15em;"></div>
<div style="margin:0; padding: 50; background-color: rgba(0,0,0,0.5); min-hight:100%; min-width:100%" >
    <h1 style="color:white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);" >Architecting Multi-modal LLMs</h1>
    <p style="color:white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);" > MSA 8700 — Module 12</p>
</div>

{{% note %}}
Welcome to Module 12. Up to this point in the course, every system we have built — RAG pipelines, agentic workflows, knowledge graphs — has operated exclusively on text. That changes today. The world our agents need to reason about is not made of text; it is made of images, sounds, documents with complex layouts, and video. A financial analyst does not read a quarterly report as a stream of characters — they read charts, scan tables, and interpret figures spatially. A quality-control agent on a factory floor needs to see, not read. Today we examine how to give our AI systems that same perceptual breadth.

This session covers multimodal large language models end-to-end: the engineering that makes them work, and the architectural patterns that make them useful in production.

Here is the roadmap for the next two hours:

1. **The Signal Topography** — Why text-only models hit a perceptual wall, and how the convergence of vision encoders with language models in 2023-2025 created an entirely new class of capability.

2. **Modality Taxonomy** — A precise look at text, images, audio, video, and documents as distinct signal types, each with its own encoding demands and information density.

3. **Vision Language Model Architecture** — The three-stage pipeline (vision encoder, projection layer, LLM backbone) that underpins every modern VLM from LLaVA to GPT-4o. We will work through the patch count formula, CLIP's contrastive training objective, the MLP-vs-Q-Former projection trade-off, and the four fusion strategies that determine how deeply vision and language interact.

4. **Visual Grounding** — How visual tokens act as persistent anchors during generation, enabling spatial, semantic, and temporal grounding. We will also cover prompting strategies that materially improve VLM accuracy.

5. **Multimodal RAG** — The core architectural decision between modality conversion (Path A) and native multimodal embedding (Path B). We will examine ColPali's late-interaction retrieval mechanism in detail and the hybrid indexing architecture (BM25 + dense vectors + tensor index with Reciprocal Rank Fusion) used in production systems.

6. **Multimodal Agentic Patterns** — Four design patterns that connect multimodal perception to the agentic loop: visual perception driving planning, multimodal tool use, cross-modal memory and retrieval, and VLM-based evaluation and verification.

7. **The 2026 Model Landscape** — A practical survey of the models available today, from GPT-4o and Gemini 2.5 Pro to the open-weight Qwen2.5-VL and InternVL3 families, with specific deployment recommendations for our course cluster.

By the end of this session, you will understand the full engineering stack from raw pixels to grounded agent actions, and you will have the vocabulary to make informed architectural decisions for the multimodal components of your capstone projects.
{{% /note %}}

***
<!-- 
{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_00.png" >}}
<h1></h1>
<!-- Title 

*** -->

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_01.png" >}}
<h1></h1>

***

## Why Multimodal?

- Text-only LLMs cannot reason about visual content — photos, scans, diagrams are opaque
- Document text extraction destroys spatial layout (table alignment, figure positioning)
- Audio signals (prosody, speaker identity, environmental sounds) are inaccessible
- Video — the richest information channel — is entirely unavailable to text-only models
- The world is multimodal; intelligent agents must perceive it as such
- Multimodal perception maps directly to the **perception stage** of the agent loop
- Convergence of vision encoders + language models (2023-2025) produced emergent capabilities neither system has alone
- Unlocks new agent behaviors: dashboard diagnosis, visual document ingestion, video understanding

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_02.png" >}}
<h1></h1>

***

## Modality Taxonomy

- **Text**: Discrete, sequential, symbolic; 32K-128K vocabulary; highest info density per token
- **Images**: Continuous 2D (H x W x C); decomposed into P x P patches; 256-9,216 tokens per image vs. 50-100 for equivalent text description
- **Audio**: 1D waveform → Mel spectrogram (2D) for processing; carries prosody, speaker identity, emotion beyond lexical content
- **Video**: Temporal frame sequence + audio; requires spatial AND temporal attention; O(N<sup>2</sup>) scaling in both dimensions; subsampled in practice (1-4 fps)
- **Documents**: Fused modality — text + layout + images + tables; layout-aware encoders (LayoutLM) or treat pages as images via VLM
- **Other**: IoT sensors, IMU, depth maps (e.g., Meta's ImageBind — 6-modality unified embedding)

***

{{< slide content-image="/imgs/MMLLM-SFTP.png" >}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_03.png" >}}
<h1></h1>

***

## VLM Three-Stage Architecture

- **Stage 1 — Vision Encoder (ViT/CLIP)**: Splits image into P x P patches → linear projection → position embeddings → transformer encoder layers
- **Stage 2 — Projection / Adapter Layer**: Maps vision encoder output dimensionality to LLM embedding space (e.g., 1024d → 4096d); MLP or Q-Former
- **Stage 3 — LLM Backbone + Token Fusion**: Visual tokens prepended to text tokens → unified causal self-attention; no LLM architecture changes needed
- **Training Phase 1**: Freeze vision encoder, train projection layer on image-caption pairs (alignment)
- **Training Phase 2**: Fine-tune projection + LLM (or LoRA) on visual instruction-following datasets

***

## Stage 1: Vision Encoder (ViT / CLIP)

The vision encoder transforms a raw image into a sequence of dense feature vectors. The dominant architecture is the Vision Transformer (ViT), which operates by splitting an input image of resolution H × W into a grid of non-overlapping patches, each of size P × P pixels. For a standard ViT-L/14 configuration with input resolution 224 × 224 and patch size P = 14, this produces N = (H/P) × (W/P) = 16 × 16 = 256 patches. Each patch is flattened into a vector of dimension P² × C = 14² × 3 = 588 and linearly projected to a d-dimensional embedding (1024 for ViT-L). Learnable position embeddings are added to each patch token to encode spatial location. A special [CLS] token is prepended to the sequence to aggregate global image semantics. The resulting sequence of N + 1 tokens is processed through L transformer encoder layers with multi-head self-attention.

***

## Stage 2: Projection / Adapter Layer

The vision encoder outputs embeddings in its own dimensionality (e.g., 1024d for ViT-L/14, 1408d for EVA-CLIP), which must be projected to match the LLM backbone's token embedding space (e.g., 4096d for LLaMA-7B, 5120d for LLaMA-13B). Two dominant approaches exist for this alignment — Linear MLP Projection and Q-Former — which we will examine in detail on the next slides.

***

## Stage 3: LLM Backbone and Token Fusion

 The projected visual tokens are introduced into the LLM's input sequence alongside text tokens. 
 
 In the simplest formulation, visual tokens are prepended to the text token sequence: the LLM receives $[V₁, V₂, ..., V_N, T₁, T₂, ..., T_M]$ as its input, where $V_i$ are visual tokens and $T_j$ are text tokens. 
 
 The LLM's causal self-attention mechanism then operates over this unified sequence — every text token can attend to all visual tokens and all preceding text tokens. Generation is autoregressive: the model predicts the next text token conditioned on all visual tokens and all previously generated text tokens. This fusion mechanism requires no architectural modification to the LLM itself — only the input representation changes.

***

## Stage 3: LLM Backbone and Token Fusion (cont'd)

The training procedure typically follows a two-phase approach.
- Phase 1: Pre-training alignment — the vision encoder is frozen and only the projection layer is trained on large-scale image-caption pairs (e.g., 558K filtered pairs from CC3M in LLaVA). The objective is to align the visual feature space with the LLM's token space.
- Phase 2: Visual instruction tuning — the projection layer and LLM (or LoRA adapters on the LLM) are jointly fine-tuned on curated instruction-following datasets that pair images with multi-turn question-answer conversations.

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_04.png" >}}
<h1></h1>

***

## Patch Count and Computational Cost

- **Patch count formula**: N = (H / P) x (W / P) — determines tokens per image
- Standard: 224x224, P=14 → **256 patches** (manageable)
- High-res: 1344x1344, P=14 → **9,216 patches** (expensive, O(N<sup>2</sup>) attention)
- Cost reduction strategies:
  - **Dynamic resolution** — resize to minimum needed for the task
  - **Patch merging** — combine adjacent patches in later layers
  - **Windowed attention** — local windows + periodic global attention → near-linear scaling
- Image tokens have much lower info density than text tokens — central design challenge
- Vision encoder pre-trained via CLIP contrastive learning before connecting to LLM

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_05.png" >}}
<h1></h1>

***

## CLIP: Contrastive Language-Image Pre-training

- Two parallel encoders: **ViT** (images) + **text transformer** (captions) → shared d-dimensional space
- Trained on **400M image-caption pairs** via InfoNCE contrastive loss
- B x B similarity matrix per batch; loss pushes matching pairs together, non-matching apart
- Temperature parameter τ controls distribution sharpness (learned, init 1/0.07)
- Large batch sizes essential (**32,768**) — negative pairs scale as B<sup>2</sup> - B
- Creates shared embedding space enabling:
  - Zero-shot classification (embed class names, find nearest image)
  - Cross-modal retrieval
  - Linguistically-aligned visual features for VLMs
- Limitation: **77-token** text context; LLM2CLIP (2024) extends to thousands of tokens

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_06.png" >}}
<h1></h1>

***

## MLP Projection vs. Q-Former

- **MLP Projection (LLaVA-style)**:
  - 2-layer MLP + GELU activation; ~20M parameters
  - 1:1 patch-to-token mapping — preserves all spatial detail
  - Trade-off: all 256+ patch tokens passed to LLM, consuming context window
- **Q-Former (InstructBLIP-style)**:
  - Cross-attention with 32-64 learnable query tokens
  - Compresses 256+ visual tokens → 32-64 tokens
  - Queries selectively attend to most informative patches
  - Pre-trained in 2 stages: vision-language representation, then generative learning
- **Key trade-off**: MLP preserves spatial fidelity (better for OCR, small objects); Q-Former saves context (enables more images per window)

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_07.png" >}}
<h1></h1>

***

## Four Fusion Strategies

- **Early Fusion** (LLaVA, Qwen-VL): All visual + text tokens in single sequence from layer 1; richest cross-modal attention; cost O((V+T)<sup>2</sup>) per layer
- **Late Fusion**: Separate streams until final layers; computationally efficient; weak cross-modal reasoning — only for coarse visual tasks
- **Cross-Attention Fusion** (Flamingo): Dedicated cross-attention heads at intervals (e.g., every 4th layer); Perceiver Resampler keeps visual token count fixed; scales well for video
- **Hybrid Fusion** (Gemini, GPT-4o): Combines strategies — early fusion for critical visual tokens, sparse cross-attention for full set; balances cost and reasoning depth

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_08.png" >}}
<h1></h1>

***

## Visual Grounding

- Visual tokens are **persistent anchors** in the attention window throughout generation
- **Spatial Grounding**: High attention on specific patch regions → bounding box reasoning, relative position, anomaly localization; fidelity depends on patch resolution
- **Semantic Grounding**: Visual tokens shift output distribution toward visually-consistent language (distributional effect, not explicit reasoning)
- **Temporal Grounding** (video): Frame-level attention aligns text to specific time segments
- **Prompting tip**: Question-before-image yields **5-10% higher accuracy** (attentional priming — model knows what to look for before seeing the image)
- Four context injection patterns:
  - Image-as-evidence | Image-as-query | Image-as-output | Interleaved modalities

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_09.png" >}}
<h1></h1>

***

## Multimodal RAG: Two Paths

- Standard text RAG **fails** on documents with charts, diagrams, tables — visual content discarded or reduced to lossy OCR artifacts
- **Path A — Modality Conversion**:
  - OCR + VLM captioning + layout parsing → text → standard text RAG pipeline
  - Pro: Compatible with existing infrastructure
  - Con: Significant information loss (chart relationships, table alignment, dense visuals)
- **Path B — Native Multimodal Embedding**:
  - CLIP / ColPali / Cohere Embed v4 → shared vector space for text + images
  - Pro: Preserves full visual semantics; VLM sees original charts and tables
  - Con: Requires multimodal embedding model + tensor-capable index

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_10.png" >}}
<h1></h1>

***

## ColPali: Late-Interaction Visual Retrieval

- **ColBERT-inspired** architecture: each patch token gets its own **128-d embedding** (not one vector per image)
- Relevance score: **score(q, d) = Σ<sub>i</sub> max<sub>j</sub> sim(q<sub>i</sub>, d<sub>j</sub>)**
  - Per-query-token max similarity across all document patches, then summed
- Enables **region-specific matching** — "revenue table" matches table area on page, ignoring unrelated regions
- Operates on **full PDF pages** — no OCR, text extraction, or chunking needed
- Paradigm shift: render documents as images, search the visual representation directly
- Requires **tensor-capable index** (Qdrant, Vespa) — one document = multiple vectors, not one

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_11.png" >}}
<h1></h1>

***

## Hybrid Indexing Architecture

- Three parallel indices for maximum recall:
  - **BM25 / Full-Text**: Keyword exact-match; captures acronyms, entity names, rare terms dense embeddings miss
  - **Dense Vector** (HNSW): Semantic similarity; paraphrase and concept matching; O(log N) ANN search, >95% recall
  - **Tensor Index**: Per-patch embeddings (ColPali); fine-grained visual region matching
- Results fused via **Reciprocal Rank Fusion (RRF)**: score = Σ 1/(c + rank<sub>i</sub>(d)), c=60
- Optional **VLM reranker** for cross-modal reasoning over top-k results
- Course cluster stack: **Qdrant + OpenCLIP + Ollama**

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_12.png" >}}
<h1></h1>

***

## Multimodal Perception in the Agentic Loop

- Multimodal perception maps to the agent cycle: **perception → planning → memory → execution**
- **Perception** ("Eyes"): Vision encoder processes screenshots, camera feeds, document scans, satellite imagery
- **Signal Routing** ("Optic Nerve"): Projection layer bridges vision encoder → LLM token space
- **Planning / Memory** ("Prefrontal Cortex"): LLM reasons over fused visual + text tokens to select actions
- **Execution**: Actions produce new visual states → **closed perception-action loop**
- Key insight: VLMs enable agents to navigate GUIs, verify visual outputs, process complex documents, and reason spatially — not just chatbots that can see

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_13.png" >}}
<h1></h1>

***

## Four Multimodal Agentic Patterns

- **Pattern 1 — Visual Perception → Planning**: VLM extracts structured info from visual input → feeds planner (e.g., SEC 10-K pages → entity extraction → Neo4j knowledge graph)
- **Pattern 2 — Multimodal Tool Use**: Agent calls tools with visual I/O (chart generators, browser screenshots, GIS tiles); VLM interprets visual output → next action
- **Pattern 3 — Cross-Modal Memory**: Multimodal vector store (text + image embeddings); retrieval across both spaces with RRF fusion; course stack: Qdrant + Ollama + Qwen2.5-VL
- **Pattern 4 — Multimodal Evaluation**: VLM judge evaluates generated visual outputs for accuracy, quality, compliance; closes the generation-evaluation loop (e.g., verify chart matches source data)

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_14.png" >}}
<h1></h1>

***

## 2026 Model Landscape

- **GPT-4o** (OpenAI): Proprietary, 128K ctx; native audio I/O; best cross-modal reasoning
- **Gemini 2.5 Pro** (Google): Proprietary, 1M ctx; strongest video understanding; natively interleaved modalities
- **Qwen2.5-VL 72B** (Alibaba): Open, 128K ctx; matches GPT-4o on MMMU (83.0% vs 69.1%); LoRA fine-tunable; **course cluster recommended**
- **Qwen2.5-VL 7B**: Open, 128K ctx; fast interactive inference; ~16 GB VRAM
- **InternVL3 38B** (Shanghai AI Lab): Open, 64K ctx; top OCR + chart understanding
- **ImageBind** (Meta): 6-modality unified embedding (text, image, audio, video, IMU, depth)
- **Course cluster**: Qwen2.5-VL 7B for interactive, 72B for max quality; OpenCLIP + Qdrant for retrieval

***

