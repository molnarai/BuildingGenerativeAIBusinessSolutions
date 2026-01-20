---
date: 2026-01-26
classdates: 'Monday 2026-01-26, Wednesday 2026-01-21'
draft: false
title: 'Generative AI & LLMs'
weight: 20
numsession: 2
---


This session provides a comprehensive overview of artificial intelligence (AI), focusing on the evolution, concepts, and applications of Generative AI. The session explores topics such as the history of AI, different types of machine learning, neural networks, deep learning, large language models, and AI agents. It examines various generative models, including Generative Adversarial Networks (GANs) and Variational Autoencoders (VAEs). The session emphasizes prompt engineering and transfer learning techniques for optimizing the performance of these models.

<!-- more -->
<!--     -->

Slide deck posted on the [iCollege](https://icollege.gsu.edu/) class site.

<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Evaluating+Large+Language+Models_2.wav" type="audio/wav">
    Your browser does not support the audio element.
</audio>

<!-- Listen to the [AI-generated podcast](https://notebooklm.google.com/notebook/075a14f0-3dc5-4965-bb03-8cd9650f4f7b/audio) (Compare the content to the slides to the AI-generated podcast). -->

### Suggested Reading
- Textbook [**Hands-On Large Language Models**](https://go.oreilly.com/georgia-state-university/library/view/hands-on-large-language/9781098150952/) by Jay Alammar and Maarten Grootendorst
    - [Chapter 1. An Introduction to Large Language Models](https://go.oreilly.com/georgia-state-university/library/view/hands-on-large-language/9781098150952/ch01.html)
    - [Chapter 6. Prompt Engineering](https://go.oreilly.com/georgia-state-university/library/view/hands-on-large-language/9781098150952/ch06.html#choosing_a_text_generation_model)
- Textbook [**Fundamentals of Machine Learning for Predictive Data Analytics**](https://research.ebsco.com/c/niwdz3/ebook-viewer/pdf/ijxy5p6dqn/section/lp_Cover) by John D. Kelleher, Brian Mac Namee and Aoife D'Arcy
    - [Chapter 8. Deep Learning](https://research.ebsco.com/c/niwdz3/ebook-viewer/pdf/ijxy5p6dqn/section/lp_381)


### Highlights
This session emphasizes several key insights about Generative AI:

*   **Generative AI is a rapidly evolving field with the potential to revolutionize numerous industries.** Generative AI models, trained on vast datasets, can produce novel and realistic content, including text, images, videos, and audio. Applications range from content creation and drug discovery to personalized recommendations and even generating creative text like poems or code.

*   **Large Language Models (LLMs) are foundational to Generative AI.**  LLMs are trained on massive text datasets using self-supervised learning techniques, enabling them to understand and generate human-like text. Architectures like transformers, incorporating attention mechanisms, facilitate capturing long-range dependencies in text.

*   **Fine-tuning and alignment are crucial steps in developing effective and responsible LLMs.** Fine-tuning tailors pre-trained models to specific tasks, while alignment techniques, often involving human feedback, ensure model outputs adhere to human values and ethical standards.

*   **Prompt engineering plays a vital role in harnessing the capabilities of LLMs.**  The quality of prompts directly impacts the relevance and accuracy of model outputs. Effective prompts provide clear instructions, context, and desired output format, guiding the model towards producing desired results.

*   **Transfer learning is a powerful technique that leverages pre-trained models to expedite and enhance the development of new models.** This approach applies knowledge gained from one task to another related task, reducing training time and improving performance. Transfer learning finds applications in both computer vision, such as image classification and object detection, and natural language processing, such as sentiment analysis and language translation.

*   **The development of AI agents, powered by LLMs and augmented with external knowledge, holds significant potential for creating intelligent systems capable of autonomous task execution and human-like interaction.**. These agents can access external databases, adapt to dynamic environments, and continuously learn, making them versatile for applications ranging from personal assistants to components of complex autonomous systems.

<!-- 

### Outline 
*   **What is Artificial Intelligence?**
    *   Definitions of AI from experts like Kurzweil and Luger & Stublefield.
    *   Types of AI: Artificial Narrow Intelligence (ANI), Artificial General Intelligence (AGI), and Artificial Super Intelligence (ASI).
    *   Different approaches to AI, including thinking like humans, thinking rationally, acting like humans, and acting rationally.
*   **History of Artificial Intelligence**
    *   Early AI research in the 1950s-1960s focusing on symbolic processing and rule-based systems.
    *   Development of expert systems in the 1970s-1980s, like MYCIN for medical diagnosis.
    *   The AI winter and the rise of machine learning in the late 1980s-1990s.
    *   Impact of the internet and big data in the 2000s, leading to advancements in search engines and recommendation systems.
    *   Deep learning breakthroughs in the 2010s, revolutionizing image and speech recognition.
    *   AI integration into business strategies and operations in the 2020s.
    *   Emergence of generative AI and its potential impact in the future.
*   **Generative AI**
    *   Definition of Generative AI as a subset of AI that can create new content like text, images, videos, and audio.
    *   Training process of Generative AI models on large datasets to learn patterns and features.
    *   Applications of Generative AI in content creation, drug discovery, personalized recommendations, and other fields.
    *   Exploration of different neural network architectures used in Generative AI, such as GANs, VAEs, and transformer-based models.
*   **Machine Learning**
    *   Explanation of supervised, unsupervised, and reinforcement learning.
    *   Examples of each machine learning type and their applications.
*   **Neural Networks**
    *   Inspiration from biological neural networks in the human brain.
    *   Structure of neural networks with interconnected nodes (neurons) in layers.
    *   Learning capability of neural networks through adjusting connection weights.
    *   Applications of neural networks in image recognition, speech recognition, natural language processing, and autonomous vehicles.
    *   Training process using backpropagation and optimization techniques.
    *   Challenges and risks associated with training neural networks, such as overfitting, underfitting, and vanishing gradients.
*   **Deep Learning**
    *   Deep learning networks characterized by multiple layers of interconnected nodes.
    *   Ability to extract abstract features from input data through hierarchical layers.
    *   Use of backpropagation for training and optimizing weights.
    *   Applications of deep learning in image recognition, speech recognition, and natural language processing.
    *   Differences between deep neural networks and regular neural networks in depth, feature learning, complexity, computational resources, and performance.
    *   Historical overview of deep neural network architectures and their evolution.
*   **Data Sources**
    *   Discussion of image and text data sources used for training generative models.
    *   Examples of popular image datasets like ImageNet, COCO, and CIFAR.
    *   Examples of text datasets like BooksCorpus, English Wikipedia, Common Crawl, and Reddit.
*   **Large Language Models (LLMs)**
    *   Building LLMs, including data cleaning, tokenization, position encoding, and transformer architectures.
    *   Model pre-training on massive unlabeled text data using self-supervised learning techniques.
    *   Common self-supervised training methods: MLM, autoregressive language modeling, NSP, contrastive learning, and RTD.
    *   Text corpora for pre-training, including BooksCorpus, English Wikipedia, Common Crawl, and Reddit.
    *   Fine-tuning and instruction tuning of LLMs to adapt them to specific tasks.
    *   Alignment of LLMs with human values, goals, and ethical standards.
    *   Use of Reinforcement Learning with Human Feedback (RLHF) for aligning model outputs.
*   **Generative Models**
    *   Impact of generative AI models on various domains, including vision, language, and multimodal tasks.
    *   Generative Adversarial Networks (GANs): architecture, training process, and applications in image generation, data augmentation, super-resolution, and style transfer.
    *   Variational Autoencoders (VAEs): architecture, training process, and applications in image generation, anomaly detection, feature extraction, and interpolation.
    *   Comparison of GANs and VAEs, highlighting their strengths, weaknesses, and suitability for different applications.
    *   Overview of other generative models for images.
*   **Tokenization and Embedding**
    *   Tokenization: breaking down text into smaller units (tokens).
    *   Embedding: assigning an N-dimensional vector to each token.
*   **Next Token Prediction**
    *   Process of predicting the next token in a sequence based on the input sequence and the model's training.
    *   Use of a linear layer and softmax function to produce a probability distribution over possible next tokens.
    *   Sampling methods (argmax selection, sampling, beam search) to select the next token based on probabilities.
*   **Sampling Methods**
    *   Argmax selection: choosing the token with the highest predicted probability.
    *   Sampling: randomly selecting a token based on its probability distribution, with variations like temperature sampling, top-k sampling, and top-p sampling.
    *   Beam search: maintaining multiple hypotheses (beams) and expanding them to find the most probable sequence.
*   **Sampling Temperature**
    *   Impact of temperature on token selection and randomness of generated text.
    *   Different temperature ranges and their effects on the output.
*   **Transfer Learning**
    *   Concept of reusing a pre-trained model for a new task.
    *   Benefits of transfer learning, such as reduced training time and improved performance.
    *   Common techniques: fine-tuning, feature extraction, frozen layers, learning rate annealing, layer-wise training, domain adaptation, task adaptation, and knowledge distillation.
    *   Examples of transfer learning in computer vision (image classification, object detection, facial recognition) and natural language processing (sentiment analysis, language translation, NER).
*   **Prompt Engineering**
    *   Importance of crafting effective prompts for LLMs to generate relevant and accurate outputs.
    *   Elements of a prompt: persona, instruction, context, format, audience, tone, and data.
*   **AI Agents**
    *   Capabilities of AI agents in human-like interaction, task execution, and continuous learning.
    *   Foundation of AI agents on LLMs and augmentation with external knowledge through Retrieval Augmented Generation (RAG).
 -->

