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

{{% note %}}
Text-only large language models, despite their remarkable capabilities in reasoning, generation, and instruction following, suffer from fundamental perceptual limitations. They cannot reason about visual content — a photograph, a satellite image, a medical scan, or a schematic diagram is entirely opaque to a model that processes only tokenized text. When documents containing tables, charts, and embedded figures are converted to text via extraction pipelines, the spatial layout that carries meaning — column alignment, row grouping, relative positioning of labels to data — is destroyed. Audio signals, including speech prosody, environmental sounds, and musical structure, are similarly inaccessible. Video, which combines temporal visual dynamics with synchronized audio, represents the richest and most complex information channel that text-only models cannot perceive at all.

The core motivation for multimodal large language models (MLLMs) is straightforward: the world is multimodal, and intelligent agents must perceive it as such. Human cognition integrates visual, auditory, linguistic, and tactile information continuously. An agent that can only read text is fundamentally limited in the tasks it can perform — it cannot interpret a dashboard screenshot, analyze a medical image, understand a video tutorial, or read a scanned document with complex formatting. Multimodal perception transforms the capability frontier of AI agents from text-processing systems into genuine perceptual reasoners.

In the context of agentic AI — the architectural paradigm this course explores — multimodal perception maps directly to the perception stage of the agent loop (perception → planning → memory → execution). An agent that can see, read, and hear is qualitatively more capable than one that only reads text. It can receive a screenshot of a failing dashboard and diagnose the issue. It can ingest a PDF financial filing as rendered pages, extracting tables and charts without lossy text conversion. It can watch a video demonstration and extract procedural steps. These capabilities are not incremental improvements — they unlock entirely new categories of autonomous agent behavior.

The historical trajectory is instructive. Early computer vision systems (2012–2017) developed powerful image recognition through convolutional neural networks but operated in isolation from language understanding. Separately, transformer-based language models (2018–2023) achieved remarkable text reasoning but were entirely blind to visual input. The convergence of these two streams — connecting pre-trained vision encoders to pre-trained language models through learned projection layers — represents one of the most significant architectural innovations of the 2023–2025 period. This convergence was not merely additive; the combination of visual perception with linguistic reasoning produces emergent capabilities (spatial reasoning, chart interpretation, document understanding) that neither system possesses alone.
{{% /note %}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_02.png" >}}
<h1></h1>

{{% note %}}
A modality is formally defined as a distinct channel of information characterized by its own signal structure, encoding requirements, and semantic density. Each modality imposes different computational demands on models that process it, and each carries information that cannot be fully reduced to another modality without loss.

**Text** is a discrete, sequential, symbolic modality. It is represented as a sequence of tokens drawn from a finite vocabulary, typically 32K–128K tokens for modern LLMs. Each token is mapped to a dense embedding vector of dimensionality d (commonly 4096 for models like LLaMA). Text has the highest information density per token of any modality — a single token can encode a precise concept, entity, or logical operator. The sequential structure of text is processed via causal self-attention, where each token attends to all preceding tokens in the context window. For multimodal models, the text modality serves as the "backbone" representation — all other modalities are projected into the text embedding space for unified processing.

**Images** are continuous, two-dimensional signals represented as pixel arrays — specifically, RGB tensors of shape H × W × C, where H and W are spatial dimensions and C = 3 for color channels. Unlike text, images encode spatial relationships: the relative positions of objects, their sizes, textures, and colors all carry semantic meaning. For processing by transformer architectures, images are typically decomposed into non-overlapping patches of size P × P pixels. A 224 × 224 image with P = 14 yields 256 patch tokens. The information density per patch token is substantially lower than per text token — a single image may require 256–9,216 tokens to represent, whereas the equivalent textual description might require only 50–100 tokens. This asymmetry in token efficiency is a central design challenge for multimodal architectures.

**Audio** is a continuous, one-dimensional time-domain signal — a waveform representing air pressure variations over time, typically sampled at 16 kHz (speech) to 44.1 kHz (music). For model consumption, raw waveforms are frequently transformed to frequency-domain representations via the Short-Time Fourier Transform (STFT) or Mel spectrograms, which produce 2D time-frequency matrices. These spectrograms can then be treated as single-channel images and processed by vision encoders — a key architectural insight exploited by models like Whisper. Audio carries rich information content beyond lexical content: prosody (pitch, rhythm, emphasis), speaker identity, environmental context, and emotional tone.

**Video** is the most information-dense modality: a temporal sequence of image frames (typically 24–30 fps) synchronized with an audio track. Processing video requires both spatial attention (within each frame) and temporal attention (across frames), creating a computational challenge that scales quadratically with both spatial resolution and temporal duration. Practical approaches subsample frames — selecting 1–4 fps or key frames via scene detection — and process each frame through a vision encoder before aggregating temporal information through cross-frame attention or temporal pooling. Models like Gemini 2.5 Pro natively process interleaved video frames and audio within a single context window of up to 1M tokens.

**Documents** represent a fused modality — they combine text, spatial layout, embedded images, tables, and typographic formatting into a single artifact. A PDF page is not merely text; the spatial arrangement of elements on the page carries semantic meaning. Layout-aware encoders like LayoutLM and DocFormer process documents by combining text token embeddings with 2D positional embeddings derived from bounding box coordinates. An alternative approach, increasingly prevalent in 2025–2026, treats each document page as a rendered image and processes it directly through a VLM — this bypasses the need for explicit layout parsing and handles arbitrary formatting.

Beyond the primary modalities, multimodal systems increasingly incorporate structured numerical data from IoT sensor streams, medical devices, financial time series, and tabular datasets. Meta's ImageBind demonstrates that even inertial measurement unit (IMU) data can be embedded in a shared multimodal space.
{{% /note %}}

***

{{< slide content-image="/imgs/MMLLM-SFTP.png" >}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_03.png" >}}
<h1></h1>

{{% note %}}
Modern vision language models (VLMs) share a common three-stage architecture: a vision encoder that converts images to token sequences, a projection or adapter layer that aligns the visual representation with the LLM's embedding space, and the LLM backbone that performs joint reasoning over visual and text tokens. This modular design enables leveraging pre-trained components for each stage and aligning them through relatively lightweight training.

**Stage 1: Vision Encoder (ViT / CLIP).** The vision encoder transforms a raw image into a sequence of dense feature vectors. The dominant architecture is the Vision Transformer (ViT), which operates by splitting an input image of resolution H × W into a grid of non-overlapping patches, each of size P × P pixels. For a standard ViT-L/14 configuration with input resolution 224 × 224 and patch size P = 14, this produces N = (H/P) × (W/P) = 16 × 16 = 256 patches. Each patch is flattened into a vector of dimension P² × C = 14² × 3 = 588 and linearly projected to a d-dimensional embedding (1024 for ViT-L). Learnable position embeddings are added to each patch token to encode spatial location. A special [CLS] token is prepended to the sequence to aggregate global image semantics. The resulting sequence of N + 1 tokens is processed through L transformer encoder layers with multi-head self-attention.

**Stage 2: Projection / Adapter Layer.** The vision encoder outputs embeddings in its own dimensionality (e.g., 1024d for ViT-L/14, 1408d for EVA-CLIP), which must be projected to match the LLM backbone's token embedding space (e.g., 4096d for LLaMA-7B, 5120d for LLaMA-13B). Two dominant approaches exist for this alignment — Linear MLP Projection and Q-Former — which we will examine in detail on the next slides.

**Stage 3: LLM Backbone and Token Fusion.** The projected visual tokens are introduced into the LLM's input sequence alongside text tokens. In the simplest formulation, visual tokens are prepended to the text token sequence: the LLM receives [V₁, V₂, ..., V_N, T₁, T₂, ..., T_M] as its input, where V_i are visual tokens and T_j are text tokens. The LLM's causal self-attention mechanism then operates over this unified sequence — every text token can attend to all visual tokens and all preceding text tokens. Generation is autoregressive: the model predicts the next text token conditioned on all visual tokens and all previously generated text tokens. This fusion mechanism requires no architectural modification to the LLM itself — only the input representation changes.

The training procedure typically follows a two-phase approach. Phase 1: Pre-training alignment — the vision encoder is frozen and only the projection layer is trained on large-scale image-caption pairs (e.g., 558K filtered pairs from CC3M in LLaVA). The objective is to align the visual feature space with the LLM's token space. Phase 2: Visual instruction tuning — the projection layer and LLM (or LoRA adapters on the LLM) are jointly fine-tuned on curated instruction-following datasets that pair images with multi-turn question-answer conversations.
{{% /note %}}


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

{{% note %}}
The patch count formula is central to understanding computational cost: N = (H / P) × (W / P). This determines how many tokens a single image will inject into the LLM's context window.

For standard input — a 224 × 224 image with P = 14 — this yields 256 patches. Each patch is flattened into a vector of dimension P² × C = 14² × 3 = 588 and linearly projected to a d-dimensional embedding (1024 for ViT-L). This is manageable and fits comfortably within modern context windows.

For high-resolution images — for example, 1344 × 1344 with P = 14 — this yields N = 9,216 patch tokens, a substantial addition to the LLM's context window. Self-attention over these tokens has O(N²) complexity, making high-resolution processing computationally expensive.

Several strategies address this cost:
- **Dynamic resolution**: resize images to the minimum resolution needed for the task, reducing token count proportionally.
- **Patch merging**: combine adjacent patches in later layers to reduce token count while preserving information from the original resolution.
- **Windowed attention**: restrict attention to local windows with periodic global attention, reducing the quadratic scaling to near-linear for the vision encoder portion.

The information density per patch token is substantially lower than per text token. A single image may require 256–9,216 tokens to represent, whereas the equivalent textual description might require only 50–100 tokens. This asymmetry in token efficiency is a central design challenge for multimodal architectures — it directly affects how many images can fit in a context window and how expensive multi-image reasoning becomes.

Pre-training of the vision encoder is typically performed via contrastive learning on large-scale image-text pair datasets, as in CLIP. This gives the encoder semantically meaningful features before it is ever connected to an LLM.
{{% /note %}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_05.png" >}}
<h1></h1>

{{% note %}}
CLIP, introduced by Radford et al. (2021), established the foundational approach to learning aligned visual and textual representations through contrastive pre-training. The architecture consists of two parallel encoders: a Vision Transformer (or ResNet variant) that maps images to a d-dimensional embedding, and a text transformer that maps captions to the same d-dimensional space. Both encoders are trained simultaneously on a dataset of 400 million (image, caption) pairs collected from the internet.

The training objective is the InfoNCE contrastive loss. Given a batch of B (image, caption) pairs, CLIP computes the cosine similarity between every image embedding and every caption embedding in the batch, producing a B × B similarity matrix. The loss encourages the diagonal entries (matching pairs) to have high similarity while off-diagonal entries (non-matching pairs) have low similarity. Formally, for image embedding z_i and text embedding z_t, the loss for the image-to-text direction is:

L_i2t = -log( exp(sim(z_i, z_t) / τ) / Σ_j exp(sim(z_i, z_j) / τ) )

where sim(a, b) = (a · b) / (||a|| · ||b||) is the cosine similarity and τ is a learned temperature parameter that controls the sharpness of the distribution. The symmetric text-to-image loss is computed analogously, and the total loss is the average of both directions.

This contrastive objective creates a shared embedding space where semantically related images and texts are nearby in cosine distance, enabling zero-shot classification (embed class names as text, find nearest image), cross-modal retrieval, and — critically for VLMs — high-quality visual features that are already linguistically aligned.

The temperature parameter τ plays a crucial role: too high a temperature produces a uniform distribution where all pairs appear equally similar; too low a temperature produces a distribution that is too peaked, making training unstable. CLIP learns τ as a log-parameterized scalar initialized to 1/0.07.

Large batch sizes (32,768 in the original CLIP) are essential because the number of negative pairs scales as B² - B, providing more discriminative signal per gradient step.

CLIP's text encoder has a notable limitation: a 77-token maximum context length, which constrains the complexity of text descriptions it can encode. LLM2CLIP (Microsoft Research, 2024) addresses this by replacing CLIP's text encoder with a full LLM fine-tuned via caption contrastive loss, extending the effective text context to thousands of tokens while maintaining compatibility with CLIP's visual encoder.
{{% /note %}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_06.png" >}}
<h1></h1>

{{% note %}}
The vision encoder outputs embeddings in its own dimensionality, which must be projected to match the LLM backbone's token embedding space. Two dominant approaches exist for this alignment, and the choice between them has major implications for token efficiency and reasoning quality.

**Linear MLP Projection (LLaVA-style).** A simple two-layer MLP with a GELU activation maps each visual token independently from the encoder's dimensionality to the LLM's dimensionality. The transformation can be expressed as: h = W₂ · GELU(W₁ · v + b₁) + b₂, where v is the vision encoder output for a single patch, W₁ and W₂ are learned weight matrices, and h is the projected token in the LLM's embedding space. This approach, used in LLaVA, is lightweight (~20M parameters for a 1024→4096 projection), fast to train, and preserves the one-to-one correspondence between patch tokens and projected tokens. The trade-off is that it performs no cross-token compression — all 256+ patch tokens are passed to the LLM, consuming context window capacity.

**Q-Former (Querying Transformer, InstructBLIP-style).** Introduced in BLIP-2 and used in InstructBLIP, the Q-Former is a cross-attention module that uses a fixed set of N_q learnable query tokens (typically 32–64) to attend to the full set of visual feature tokens via cross-attention. The queries extract the most salient information from the visual features and compress the representation from 256+ tokens down to N_q tokens. This dramatically reduces the number of tokens injected into the LLM context, at the cost of potential information loss for fine-grained spatial details.

The cross-attention mechanism computes: Attention(Q, K, V) = softmax(Q · K^T / sqrt(d_k)) · V, where Q comes from the learnable query tokens and K, V come from the vision encoder output. This allows the Q-Former to selectively attend to the most informative visual patches.

The Q-Former is pre-trained in two stages: vision-language representation learning (image-text matching, contrastive, and generative objectives) and vision-to-language generative learning.

The key architectural trade-off: MLP projection preserves all spatial detail but consumes more context; Q-Former compresses aggressively (256 tokens down to 32) enabling more images per context window, but may lose fine-grained details critical for tasks like OCR or small-object detection.
{{% /note %}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_07.png" >}}
<h1></h1>

{{% note %}}
The mechanism by which visual and textual token sequences are combined within the model has significant implications for computational cost, cross-modal reasoning depth, and scalability. Four primary fusion strategies are employed in current architectures.

**Early Fusion** concatenates all patch tokens from the vision encoder with text tokens into a single sequence before the first LLM layer. Every attention head in every layer computes full cross-modal attention between all visual and all textual tokens. This provides the richest possible interaction between modalities but has a major cost: for a high-resolution image producing 4,096 patch tokens combined with a 4,096-token text prompt, the attention computation scales as O((4096 + 4096)²) = O(67M) per layer per head. Early fusion is used in LLaVA and Qwen-VL, yields strong spatial reasoning, but limits practical image resolution and multi-image inputs.

**Late Fusion** processes visual and textual tokens independently through most of the model's layers, with cross-modal interaction occurring only in the final few layers or at the output head. This is computationally efficient — the two modality streams can be processed in parallel — but produces weaker cross-modal reasoning because the model has limited capacity to ground text in visual details. Late fusion is suitable for tasks where coarse visual understanding suffices but inadequate for fine-grained visual question answering.

**Cross-Attention Fusion** (Flamingo-style) augments the LLM backbone's transformer layers with dedicated cross-attention heads that attend to a compressed visual representation (e.g., from a Perceiver Resampler that reduces hundreds of patch tokens to a fixed-size set of visual tokens). These cross-attention layers are inserted at regular intervals (e.g., every 4th layer) and are the only components that directly attend to visual features. Standard self-attention layers continue to operate over text tokens only. This design is efficient and scalable — particularly for video, where multiple frames must be processed — and the Perceiver Resampler ensures that visual token count remains fixed regardless of input resolution.

**Hybrid Fusion** is employed by modern production models, combining strategies. Lower layers may use early fusion for a small number of critical visual tokens (e.g., the [CLS] token and high-salience patch tokens), while higher layers use sparse cross-attention to the full visual feature set. This balances computational cost with cross-modal reasoning depth. Gemini and GPT-4o are believed to use hybrid fusion architectures, though their exact designs are not publicly documented.
{{% /note %}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_08.png" >}}
<h1></h1>

{{% note %}}
Visual grounding is the mechanism by which information from visual tokens influences the LLM's text generation. Because visual tokens participate in the self-attention computation across all layers (in early and hybrid fusion), every LLM layer "sees" the image. The visual tokens serve as persistent contextual anchors: they are not consumed or forgotten as generation proceeds but remain in the attention window throughout the entire generation process. Three distinct types of grounding operate in VLMs.

**Spatial Grounding.** The model attends to specific spatial regions of the image to answer location-dependent queries. This manifests as high attention weights on particular patch tokens corresponding to regions of interest. Spatial grounding enables bounding box reasoning ("Where is the defect in this X-ray?"), relative position understanding ("Is the signature above or below the date?"), and anomaly localization in medical imaging and satellite analysis. The fidelity of spatial grounding depends directly on the patch resolution — finer patches (smaller P) provide more precise localization at higher computational cost.

**Semantic Grounding.** At a higher level of abstraction, visual tokens bias the LLM's output distribution toward completions that are semantically consistent with the image content. When an image of a beach scene is present in context, the probability mass over tokens related to sand, waves, sun, and ocean increases, while tokens related to snow, mountains, or urban environments are suppressed. This is not explicit reasoning but a distributional effect: the visual tokens shift the model's prior over the vocabulary toward visually-consistent language. Semantic grounding is essential for open-ended image description, where the model must generate coherent text that faithfully reflects the image's high-level content without being prompted about specific visual elements.

**Temporal Grounding.** In video processing, temporal grounding aligns text to specific temporal segments of the video via frame-level attention. The model can identify "the moment when the speaker raises their hand" by attending strongly to the frame tokens from the relevant time segment. Temporal grounding requires frame-level indexing in the token sequence and is most effective when frames are sampled at sufficient density to capture the events of interest. Models that process video as a sequence of frame embeddings can perform temporal reasoning by computing attention patterns that peak at specific frame positions — analogous to how text attention peaks at relevant words during question answering.

**Prompting Strategies for Visual Reasoning.** Empirical research has demonstrated that prompt ordering significantly affects VLM performance on analytic tasks. Specifically, placing the question before the image in the prompt sequence yields 5–10% higher accuracy compared to image-first ordering on tasks requiring detailed visual analysis. The mechanism is attentional priming: when the question appears first, the LLM processes the question tokens and establishes which concepts and relationships are relevant. When the visual tokens subsequently enter the attention window, the model's attention heads are already primed to attend to the relevant visual features, leading to more focused and accurate visual extraction.

Four primary context injection patterns characterize how images interact with text in multimodal prompts: Image-as-evidence (the image provides supporting context for a text query), Image-as-query (the image is the primary query and text provides the task instruction), Image-as-output (the model generates or references an image as part of its response), and Interleaved modalities (images and text are interspersed throughout the prompt in natural order, enabling few-shot learning with visual examples).
{{% /note %}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_09.png" >}}
<h1></h1>

{{% note %}}
The standard Retrieval-Augmented Generation (RAG) pipeline operates as follows: a user query is embedded into a dense vector via a text embedding model, approximate nearest neighbor (ANN) search retrieves the top-k text chunks from a vector index, and these chunks are injected into the LLM's context window as grounding evidence for generation. This pipeline works well when the knowledge base is purely textual. However, it fails fundamentally when the corpus contains documents with embedded images, charts, diagrams, and tables — the visual content is either discarded entirely during text extraction or reduced to meaningless OCR artifacts that lose the spatial and visual semantics that make the content informative.

Consider a concrete failure case: an SEC 10-K filing contains a bar chart showing quarterly revenue trends. Standard text extraction produces nothing from this chart — it is a raster image embedded in the PDF. Even if OCR extracts axis labels and data values, the spatial relationships (which bar is taller, the trend direction, the relative magnitude of changes) are lost. A text RAG system queried about "revenue growth trajectory" would retrieve narrative text passages but miss the most informative evidence in the document.

**Path A — Modality Conversion.** The first approach converts all non-text content to text before indexing. OCR extracts text from images and scanned pages. VLM captioning generates textual descriptions of charts and diagrams. Layout parsers reconstruct table structure as markdown or HTML. The resulting text is then processed through the standard text RAG pipeline. This approach has the advantage of compatibility with existing text RAG infrastructure — no changes to the embedding model, vector index, or retrieval logic are required. However, information loss is significant: chart captions cannot fully capture the data relationships visible in the visualization; table OCR frequently misaligns columns; and dense visual content like heat maps, scatter plots, and technical diagrams resist accurate textual description.

**Path B — Native Multimodal Embedding.** The second approach embeds images directly as vectors in a shared embedding space alongside text. Models like CLIP, ColPali, and Cohere Embed v4 produce embeddings where text and images coexist in the same vector space — a query text can retrieve relevant images, and an image query can retrieve relevant text. These embeddings are stored in a multimodal-capable vector database. Retrieval returns mixed text-and-image results, which are then passed to a VLM for grounded generation. This approach preserves full visual semantics — the VLM sees the original chart, diagram, or table page rather than a lossy textual approximation. The trade-off is that it requires a multimodal embedding model and a tensor-capable index (for late-interaction models like ColPali), adding infrastructure complexity.
{{% /note %}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_10.png" >}}
<h1></h1>

{{% note %}}
ColPali deserves particular attention for its novel retrieval mechanism. Unlike standard embedding models that produce a single vector per document or image, ColPali uses a late interaction architecture inspired by ColBERT. Each patch token in the vision encoder's output receives its own embedding vector of dimensionality 128. At query time, each query token computes its maximum similarity against all patch tokens in a candidate document, and these per-token maximum similarities are summed to produce the final relevance score:

score(q, d) = Σ_i max_j sim(q_i, d_j)

This fine-grained, per-patch similarity computation enables retrieval based on specific visual regions — a query about "revenue table" can match strongly with the patch tokens corresponding to the table area of a PDF page, even if the rest of the page contains unrelated content. ColPali operates at the full PDF page level, eliminating the need for text extraction or chunking entirely. This represents a paradigm shift: instead of extracting text from documents and searching text, you render documents as images and search the visual representation directly.

The ColBERT-style architecture means that each patch token receives its own 128-dimensional embedding vector. This is in contrast to models like CLIP that produce a single vector per image. The per-patch approach preserves spatial information in the retrieval step itself — the system knows not just that a document is relevant, but which regions of the document matched which parts of the query.

The practical implication is significant: ColPali can retrieve the specific page of a multi-hundred-page PDF that contains a relevant chart, table, or diagram, purely based on visual similarity with the text query — no OCR, no text extraction, no layout parsing required. The retrieved page image is then passed directly to a VLM for grounded generation, preserving the full visual fidelity of the original document.

For storage, ColPali requires a tensor-capable index (not just a standard vector index) because each document is represented by multiple vectors (one per patch), not a single vector. Databases like Qdrant and Vespa support this tensor storage natively.
{{% /note %}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_11.png" >}}
<h1></h1>

{{% note %}}
Production-grade multimodal RAG systems employ a hybrid indexing architecture that combines multiple retrieval strategies to maximize recall across different content types and query patterns. The architecture consists of three parallel indices.

**Index 1: BM25 / Full-Text Index.** A traditional inverted index providing keyword-based retrieval with TF-IDF weighting. This captures exact term matches, acronyms, entity names, and numerical values that dense embeddings may miss. Particularly important for domain-specific terminology and rare tokens that fall outside the embedding model's training distribution.

**Index 2: Dense Vector Index.** A vector index (HNSW or IVF-PQ) storing dense embeddings from a text or multimodal embedding model. This captures semantic similarity — queries that are conceptually related to documents even when they share no exact terms. Handles paraphrase, synonym, and concept-level matching. HNSW (Hierarchical Navigable Small World) graphs provide O(log N) approximate nearest neighbor search with recall rates above 95% at practical scale.

**Index 3: Tensor Index.** For late-interaction models like ColPali, a tensor index stores per-token patch embeddings for each document. This enables the fine-grained patch-level matching described above. The tensor index is particularly valuable for visual document retrieval, where relevance depends on matching specific visual regions rather than holistic document similarity.

Retrieval results from all three indices are combined via **Reciprocal Rank Fusion (RRF)**. Given ranked lists R₁, R₂, ..., R_k from k retrieval systems, the fused score for document d is:

RRF(d) = Σ_{i=1..k} 1 / (c + rank_i(d))

where c is a constant (typically 60) that dampens the influence of low-ranked documents. RRF is robust, parameter-free (beyond c), and does not require score normalization across different retrieval systems.

Optionally, a **VLM reranker** can be applied over the top-k fused results to perform cross-modal reasoning before final selection — for example, asking the VLM "Does this page contain information relevant to the query?" and using the answer to reorder results.

Technology options for implementing this architecture include Qdrant (native vector and sparse vector support, Rust-based, high performance), pgvector (PostgreSQL extension for dense vectors, good for integrated stacks), and Vespa (hybrid search with native tensor support and BM25). For the course cluster, the recommended stack is Qdrant + OpenCLIP for retrieval, running on the existing GPU nodes alongside Ollama for VLM inference.
{{% /note %}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_12.png" >}}
<h1></h1>

{{% note %}}
Multimodal perception integrates directly into the agentic AI architecture — the perception-planning-memory-execution cycle that forms the backbone of autonomous agent design. A multimodal agent does not merely process text instructions and generate text outputs; it perceives visual, auditory, and document-based inputs, reasons over them, and takes actions that may produce multimodal outputs.

The diagram shows how multimodal architectures map onto the agentic loop:

**Perception** acts as the agent's "Eyes," interpreting raw pixel data. The vision encoder receives screenshots, camera feeds, document scans, or satellite imagery and transforms them from continuous signals into structured token sequences that the rest of the system can process.

**Signal Routing** acts as the "Optic Nerve," translating visual signals into the brain's token space. This is the projection/adapter layer — it bridges the gap between the vision encoder's representation and the LLM's embedding space, ensuring that visual information arrives in a format the language model can reason over.

**Planning / Memory** acts as the "Prefrontal Cortex," reasoning over unified multi-sensory data to select actions. The LLM backbone receives the fused visual and textual tokens and performs the core reasoning — deciding what the image shows, what action to take next, what information to store in memory, and how to respond.

**Execution** is the action taken, which loops back to generate new visual states (e.g., a new browser screenshot after clicking a button, a new document page after navigating). This creates a closed perception-action loop where the agent continuously perceives, reasons, acts, and perceives again.

The key insight is that multimodal LLMs are not just chatbots that can see; they are the foundational requirement for agents to transition from text-processing systems to real-world continuous reasoners. Without visual perception, an agent cannot navigate a GUI, cannot verify that a generated chart matches the source data, cannot process a document that contains tables and figures, and cannot operate in any environment that requires spatial understanding.
{{% /note %}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_13.png" >}}
<h1></h1>

{{% note %}}
Four patterns characterize the principal ways multimodal capabilities enhance agentic behavior.

**Pattern 1: Visual Perception → Planning.** The agent receives visual input — a screenshot, camera feed, scanned document, or satellite image — and the VLM component generates a structured description, extracts entities, or identifies anomalies. This structured output feeds into the planner, which selects the next action based on the perceived state. A concrete example: an SEC filing agent ingests each page of a 10-K annual report as a rendered image. The VLM identifies and classifies regions of each page — narrative text, financial tables, risk factor lists, performance charts. Extracted entities and relationships populate a knowledge graph in Neo4j, creating a structured, queryable representation of the filing's content. The planner then routes analyst queries to the appropriate graph traversal or table lookup, with the original page images available as visual evidence for verification.

**Pattern 2: Multimodal Tool Use.** In this pattern, the agent calls an external tool whose output is visual rather than textual. The tool might generate an analytics chart, render a GIS satellite tile, produce a PDF page, or capture a screenshot of a web application. The VLM interprets the visual output, extracting data points, identifying trends, or detecting anomalies, and passes a structured summary to the next stage of the agent pipeline. Critically, both the tool input and output can be visual. This pattern is increasingly relevant as AI agents interact with graphical user interfaces. Browser agents (e.g., those built on Playwright) capture screenshots of web pages, pass them to a VLM for understanding, and generate click/type actions based on the visual interpretation. The visual interface itself becomes the API.

**Pattern 3: Cross-Modal Memory and Retrieval.** The agent maintains a multimodal vector memory store that contains text notes, associated images, figures, charts, and other visual artifacts. When a new query arrives, the retrieval system searches across both text and visual embeddings, returning heterogeneous evidence — a mix of text passages, chart images, and table screenshots. The VLM synthesizes a grounded, evidence-backed answer over this mixed evidence. This connects directly to the DAIS project infrastructure used in this course (Qdrant for vector storage, Ollama for local model inference, Qwen2.5-VL for visual understanding). Each document page is stored as both an image embedding (via OpenCLIP or ColPali) and a text embedding (from extracted text, if available). The agent's query hits both embedding spaces in parallel, and RRF fuses the results.

**Pattern 4: Multimodal Evaluation and Verification.** The agent generates a visual output — a chart, dashboard, presentation slide, or data visualization — and a VLM judge evaluates the output for visual quality, factual accuracy, and compliance with design requirements. This closes the generation-evaluation loop: the agent can iteratively refine its visual output based on the VLM judge's feedback. For example, an agent generating a quarterly earnings dashboard can submit each chart to a VLM evaluator that checks whether axis labels are correct, data points match the source data, and the color scheme meets accessibility standards. This pattern extends to code generation and testing: an agent writes code to produce a visualization, renders it, captures the output as an image, and asks a VLM judge to verify that the visualization matches the specification.
{{% /note %}}

***

{{< slide content-image="/imgs/Engineering_Multimodal_Intelligence_14.png" >}}
<h1></h1>

{{% note %}}
The multimodal LLM ecosystem has matured rapidly, with both proprietary and open-weight models achieving strong cross-modal reasoning capabilities. Here are the key models relevant to research and deployment as of early 2026:

**GPT-4o (OpenAI)** — Proprietary, 128K context. Native audio I/O, best cross-modal reasoning, unified image+text+audio processing. GPT-4o's advantage comes largely from the scale and curation of its instruction-tuning corpus rather than from architectural innovations.

**Gemini 2.5 Pro (Google)** — Proprietary, 1M context. Largest context window, strongest video understanding, natively interleaved modalities. The 1M token context enables processing of hour-long videos — a 1-hour video at 1 fps with 256 patches per frame generates 921,600 visual tokens alone.

**Qwen2.5-VL 72B (Alibaba)** — Open, 128K context. Matches GPT-4o on benchmarks (83.0% on MMMU vs. GPT-4o's 69.1%), LoRA fine-tunable, Ollama-compatible — the course cluster recommended model. Requires multi-GPU deployment (~140 GB VRAM across nodes).

**Qwen2.5-VL 7B** — Open, 128K context. For fast inference in interactive applications (e.g., agentic loops with real-time visual perception), provides strong performance at manageable GPU memory requirements (~16 GB VRAM). Recommended for the course cluster for interactive use.

**InternVL3 38B (Shanghai AI Lab)** — Open, 64K context. Strong OCR + chart understanding, layout-aware, top document benchmarks. State-of-the-art for document OCR and chart understanding tasks.

**ImageBind (Meta)** — Open, N/A. 6-modality unified embedding: text, image, audio, video, IMU, depth. Demonstrates that even inertial measurement unit data can be embedded in a shared multimodal space.

**Benchmarks and Evaluation.** The principal benchmarks include: MMBench and MMMU (general multimodal reasoning across diverse visual domains), DocVQA and ChartQA (document and chart understanding), MathVista (mathematical reasoning over visual inputs), and RealWorldQA (practical visual understanding in real-world contexts).

**On-premises deployment recommendation for the course cluster:** Two configurations based on task requirements. For interactive applications with real-time visual perception, Qwen2.5-VL 7B provides strong performance at manageable GPU memory. For maximum quality on complex visual reasoning tasks, Qwen2.5-VL 72B delivers near-GPT-4o performance but requires multi-GPU deployment. For multimodal retrieval, OpenCLIP combined with Qdrant provides a production-ready vector search pipeline that runs entirely on the existing cluster GPU nodes.
{{% /note %}}

***

