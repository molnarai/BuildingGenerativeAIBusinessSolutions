+++
date = '2025-02-10'
draft = false
title = 'Training and Finetuning of LLMs'
weight = 40
numsession = 4
+++
LLM finetuning is a powerful technique that tailors pre-trained large language models to specific tasks or domains, enhancing their performance and applicability. Unlike prompt engineering, which works within the constraints of a model's existing knowledge, finetuning involves additional training on a curated dataset to modify the model's parameters. This process allows the model to learn new patterns, adapt to specific vocabularies, and refine its understanding of particular contexts or tasks.

<!-- more -->
The finetuning process typically involves selecting a pre-trained model, preparing a high-quality dataset relevant to the target task, and training the model on this data for several epochs. During this phase, the model's weights are adjusted to better align with the specific requirements of the new task, while still retaining much of its general language understanding capabilities. This approach can significantly improve performance on specialized tasks such as sentiment analysis, text classification, or domain-specific question answering.

One of the key advantages of finetuning is its ability to create more efficient and focused models for specific applications. By adapting a general-purpose LLM to a particular domain or task, organizations can often achieve superior results compared to using the base model with prompt engineering alone. However, finetuning requires more computational resources and expertise than prompt engineering, and care must be taken to avoid overfitting or catastrophic forgetting of the model's original capabilities.

## Required Reading and Listening
Listen to the podcast ((../../podcasts/podcast-04-fine-tuning/)):
<!-- Listen to the podcast: -->

<audio controls>
    <source src="" type="audio/wav">
    Your browser does not support the audio element.
</audio>

Read the following:
1. Summary Page: [Finetuning of Large Language Models](https://www.perplexity.ai/page/finetuning-of-large-language-m-uYo8ZyfGQdijYrpM6phP_w)
2. Textbook: **Chapter 11. Fine-Tuning Representation Models for Classification** in Allamar and Grotendorst, "Hands-On Large Language Models", O'Reilly Media Inc., September 2024;
Textbook: **Chapter 5.1, 5.2, 5.3**, Huang, Ken. "Practical Guide for AI Engineers", Ind. published, May 2024.
3. Paper: [J. Devlin et al., BERT: Pre-training of Deep Bidirectional Transformers for
Language Understanding](https://arxiv.org/abs/1810.04805)

## Study Guide - Questions
1. What is the key difference between using pre-trained models in Chapter 4 versus the fine-tuning approach described in this chapter for classification tasks? 
In Chapter 4, pre-trained models were used directly for classification without any modifications to their internal weights, essentially keeping them "frozen." In contrast, this chapter explores a fine-tuning approach where both the pre-trained model and an added classification head are updated during training, allowing the model to become more specialized for the specific task at hand. This joint updating enables the model to learn task-specific representations.

2. What does **"freezing" layers** in a neural network mean during fine-tuning, and what are the potential benefits and drawbacks of doing so? 
Freezing layers in a neural network means that their weights are not updated during the training process. This can significantly reduce the computational cost and training time as fewer parameters need adjustment. However, it can also limit the model's ability to learn task-specific nuances, potentially leading to reduced performance compared to fine-tuning the entire network. The best choice depends on the specific task and available resources.

3. What is the primary benefit of using the **SetFit** framework for text classification tasks, especially when compared with other fine-tuning methods? 
The SetFit framework is primarily beneficial when dealing with limited labeled training data. Unlike traditional fine-tuning methods that often require thousands of examples, SetFit can achieve competitive performance with only a few labeled examples per class. This efficiency stems from its unique method of generating contrastive learning pairs and fine-tuning sentence embeddings which leads to strong performance with few labels.

4. Can you outline the three primary steps involved in the SetFit algorithm for **few-shot classification**? 
The SetFit algorithm involves three key steps. First, it generates positive and negative sentence pairs based on in-class and out-class selections from the limited labeled data. Second, it fine-tunes a pre-trained sentence embedding model using contrastive learning with these generated pairs. Finally, a classifier is trained on the embeddings created by the fine-tuned embedding model, which can be a simple classification head or other models.

5. Why is it advantageous to continue pre-training a pre-trained model with **masked language modeling** before fine-tuning it for a specific task like classification? 
Continuing pre-training a model with masked language modeling (MLM) before task-specific fine-tuning helps the model to further adapt to the domain-specific language and vocabulary present in your dataset. Since pre-trained models are often trained on general data, the model may not have exposure to domain-specific terminology. By using MLM, the model is fine-tuned to the specific language of your task, potentially leading to better performance and more accurate representations during classification.

6. How does **token masking** differ from **whole-word masking**, and what are the potential impacts of these differences in training? 
Token masking randomly masks individual tokens in a sentence, while whole-word masking ensures that if a part of a word is masked, then all the tokens that make up that entire word are masked together. Whole-word masking tends to produce more accurate representations as it doesn't mask parts of words without masking all of the word. Token masking is faster but less precise whereas whole word masking is a more precise and computationally expensive approach.

7. What is the main goal of **Named Entity Recognition (NER)**, and what does the NER process aim to accomplish? 
The main goal of Named Entity Recognition (NER) is to identify and classify specific named entities within unstructured text. This involves recognizing and categorizing words and phrases as belonging to predefined categories such as people, organizations, locations, or miscellaneous entities. This type of classification is done at the token level as opposed to a document-level, as we saw in regular classification.

8. In **Named Entity Recognition (NER)**, what roles do the "B-" and "I-" prefixes serve when used in labeling entities within a text? 
In NER, the "B-" prefix indicates the beginning of an entity phrase, while the "I-" prefix indicates that a token is part of an entity phrase that is already in progress. The "B-" marks the first token of the phrase and the "I-" marks any remaining tokens, allowing the NER model to distinguish between independent entities and tokens belonging to the same phrase. For example, "New York" is considered a phrase that would be labeled as B-LOC for "New" and I-LOC for "York".

## Additional Resources
- []() ...

