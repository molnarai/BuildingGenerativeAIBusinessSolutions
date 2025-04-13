+++
date = '2025-04-14'
draft = false
title = 'Image Generation, Multi-modal Generative Models'
weight = 120
numsession = 12
+++

Multimodal models, such as vision-enhanced large language models (LLMs) and diffusion models, are designed to process and integrate different types of data, including text, images, and audio. Vision LLMs combine visual and textual information to perform tasks like image captioning and visual question answering. These models use cross-attention mechanisms to align visual features with textual representations, allowing them to generate text based on images or answer questions about visual content.
<!-- mode -->
Diffusion models, in contrast, are primarily used for image generation tasks. They learn to reverse a noise-adding process to create realistic images from noise. While diffusion models are not inherently designed for text generation, they can be adapted for tasks like image-to-text generation by integrating them with text models. The training and fine-tuning processes for these models differ significantly. Vision LLMs require large datasets of paired images and text, while diffusion models rely on large image datasets with optional text descriptions.

In terms of dataset preparation, vision LLMs focus on aligning visual and textual features, emphasizing data cleaning, normalization, and tokenization. Diffusion models, on the other hand, concentrate on image normalization and augmentation to enhance visual diversity. Both models benefit from large and diverse datasets, but diffusion models are particularly sensitive to image quality and variety for generating realistic outputs. Overall, these models demonstrate the potential of multimodal approaches in enhancing performance across various tasks by leveraging the strengths of different data modalities.

**Multi-modal Large Language Models**

<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Multimodal+Large+Language+Models_+A+Survey_2.wav">
    Your browser does not support the audio element.
</audio>

**Diffusion Models**

<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Diffusion+Models%2C+Autoencoders%2C+and+Transformers_+A+Review+of+Advancements.wav">
    Your browser does not support the audio element.
</audio>


## Reading List
1. Summary Blog:  [Exploring Multi-Modal AI Models](https://www.perplexity.ai/page/exploring-multi-modal-ai-model-9H_wfcg5RwuI8Ekh7cmsdw)
2. Paper: Satyadhar Joshi. Introduction to Diffusion Models, Autoencoders and Transformers: Review of Current Advancements. 2025. [⟨hal-04999764⟩](https://hal.science/hal-04999764v1)
3. Paper: Jiayang Wu, Wensheng Gan, Zefeng Chen1, Shicheng Wan, Philip S. Yu. Multimodal Large Language Models: A Survey. [(arXiv)](https://arxiv.org/pdf/2311.13165)


The podcast was produced based on the papers:
1. [Large Language Models: A Survey](https://arxiv.org/pdf/2311.13165)
2. [Efficient Multimodal Large Language Models: A Survey](https://arxiv.org/pdf/2405.10739)
3. [Introduction to Diffusion Models, Autoencoders and
Transformers: Review of Current Advancements](https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/docs/Introduction+to+Diffusion+Models%2C+Autoencoders+and+Transformers-+Review+of+Current+Advancements.pdf) [[hal-04999764]](https://hal.science/hal-04999764v1)

### References of the "Introduction to Diffusion Models, Autoencoders and Transformers"

1. [5 Different Types Of Generative AI Models](https://www.neurond.com/blog/generative-ai-models-2).
2. [Demystifying Types of AI | AI for Decision Makers](https://www.neurond.com/blog/demystifying-types-of-ai).
3. [Diffusion Models for Generative Artificial Intelligence: An Introduction for Applied Mathematicians](https://arxiv.org/html/2312.14977v1).
4. [Diffusion Models in Generative AI: Principles, Applications, and Future Directions | Preprints.org](https://www.preprints.org/manuscript/202502.0524/v1).
5. [Diffusion Transformer (DiT) Models: A Beginner's Guide](https://encord.com/blog/diffusion-models-with-transformers/).
6. [Is synthetic data generation effective in maintaining clinical biomarkers? Investigating diffusion models across diverse imaging modalities](https://www.frontiersin.org/journals/artificialintelligence/articles/10.3389/frai.2024.1454441/full).
7. [A Guide to Popular Generative AI Models and Their Applications](https://www.webcluesinfotech.com/a-guide-to-popular-generative-ai-models-and-their-applications/).
8. [Synthetic Data Generation with Diffusion Models - Hugging Face Community Computer Vision Course](https://huggingface.co/learn/computer-vision-course/en/unit10/datagen-diffusion-models).
9. [Transformers Vs Diffusion Models | Restack.io](https://www.restack.io/p/transformer-models-answer-transformers-vs-diffusion-cat-ai).
10. [Generative AI Introduction to All Types of Gen AI Models](https://www.thirdrocktechkno.com/blog/generative-ai-introduction-to-all-types-of-gen-ai-models-2025/).
11. [What is a Generative Model? | IBM](https://www.ibm.com/think/topics/generative-model).
12. [Generating Synthetic Data with Transformers: A Solution for Enterprise Data Challenges](https://developer.nvidia.com/blog/generating-synthetic-data-with-transformers-a-solution-for-enterprise-data-challenges/), May 2022.
13. [Synthetic Data Guide: Definition, Advantages, & Use Cases](https://synthesis.ai/synthetic-data-guide/), November 2022.
14. [Exploring Generative AI Model Architectures](https://unimatrixz.com/topics/ai-art-tools/ai-models-for-generative-ai/), April 2023.
15. [Generative AI VI: Stable Diffusion, DALL-E 2, and Midjourney - Synthesis AI](https://synthesis.ai/2023/08/09/generative-ai-vi-stable-diffusion-dall-e-2-and-midjourney/), August 2023.
16. [The two models fueling generative AI products: Transformers and diffusion models](https://www.gptechblog.com/generative-ai-models-transformers-diffusion-models/), July 2023.
17. [Creating Synthetic Data with Stable Diffusion LORAS - Deep Learning Forum](https://forums.fast.ai/t/creating-synthetic-data-with-stable-diffusion-loras/111747), April 2024.
18. [Transformers to diffusion models: AI jargon explained - TechCentral](https://www.techcentral.co.za), April 2024.
19. [What is Generative AI? | IBM](https://www.ibm.com/think/topics/generative-ai), March 2024.
20. Satyadhar Joshi, "The Synergy of Generative AI and Big Data for Financial Risk: Review of Recent Developments," *IJFMR - International Journal For Multidisciplinary Research*, Vol 7(1), January 2025.
21. Staphord Bengesi et al., "Advancements in Generative AI: A Comprehensive Review of GANs, GPT, Autoencoders, Diffusion Model, and Transformers," *IEEE Access*, Vol 12, pp. 69812–69837, 2024.
22. The Tenyks Blogger, "Synthetic Data: Diffusion Models — NeurIPS 2023 Series," January 2024.
23. Minshuo Chen et al., "Opportunities and challenges of diffusion models for generative AI," *National Science Review*, Vol 11(12): nwae348, December 2024.
24. Pedro Cuenca, *Hands-on Generative AI with Transformers and Diffusion Models*, O'Reilly Media, Inc., First edition, Sebastopol, CA, 2024.
25. Darya Danikovich, "Generative AI: What Is It, Tools, Models & Use Cases," February 2024.
26. Mandeep Goyal and Qusay H Mahmoud, "A Systematic Review of Synthetic Data Generation Techniques Using Generative AI," *Electronics*, Vol 13(17):3509, January 2024.
27. Satyadhar Joshi, "Advancing innovation in financial stability: A comprehensive review of AI agent frameworks, challenges and applications," *World Journal of Advanced Engineering Technology and Science*, Vol 14(2):117–126, April 2025.
28. Satyadhar Joshi, "Implementing GenAI for Increasing Robustness of US Financial and Regulatory System," *International Journal of Innovative Research in Engineering and Management*, Vol 11(6):175–179, January 2025.
29. Kezia Jungco, "Generative AI Models: A Detailed Guide," September 2024.
30. Vaibhav Kumar, "Leveraging generative AI with transformers and stable diffusion for rich diverse dataset synthesis in AgTech," January 2024.
31. Aayush Mittal, "Understanding Diffusion Models: A Deep Dive into Generative AI," August 2024.
32. musshead, "[D] Use Cases for Diffusion Models VS GANs VS Transformers," July 2023.
33. Matteo Pozzi et al., "Generating and evaluating synthetic data in digital pathology through diffusion models," *Scientific Reports*, Vol 14(1):28435, November 2024.
34. Jason Roell, "The Ultimate Guide: RNNs vs Transformers vs Diffusion Models," April 2024.
35. Omar Sanseviero et al., *Hands-On Generative AI with Transformers and Diffusion Models*, O'Reilly Media Inc., November 2024.
36. Satyadhar Joshi, "Advancing Financial Risk Modeling: Vasicek Framework Enhanced by Agentic Generative AI," January 2025.
37. Satyadhar Joshi, "Enhancing structured finance risk models (Leland-Toft and Box-Cox) using GenAI (VAEs GANs)," *International Journal of Science and Research Archive*, Vol 14(1):1618–1630, January 2025.
38. Satyadhar Joshi, "Leveraging prompt engineering to enhance financial market integrity and risk management," *World Journal of Advanced Research and Reviews*, Vol 25(1):1775–1785, January 2025.
39. Aliona Surovtseva, "Synthetic Data Generation Using Generative AI," July 2024.
40. F Umer and N Adnan, "Generative artificial intelligence: Synthetic datasets in dentistry," *BDJ Open*, Vol 10:13–24, January 2024.

