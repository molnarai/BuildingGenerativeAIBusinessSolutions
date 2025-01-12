+++
date = '2025-01-06T18:20:46-05:00'
draft = false
title = 'Homework 2: LLM Finetuning'
weight = 20
+++
### Homework Assignment: Fine-Tuning a Large Language Model (LLM)

<p>
The objective of this assignment is to provide hands-on experience in fine-tuning a pre-trained large language model (LLM) using PyTorch.
You will begin by curating a domain-specific dataset that will serve as the training data for fine-tuning. This step involves identifying a topic of interest, collecting relevant text data, and preprocessing it to ensure it is clean and ready for use in training. Additionally, you will create a separate test dataset to evaluate the performance of the fine-tuned model.

Once the dataset is prepared, you will use the provided Python code template to perform the fine-tuning process. This task includes loading the pre-trained model, configuring hyperparameters such as batch size and learning rate, and running the training as a batch job on a GPU-enabled environment. The goal is to adapt the general-purpose LLM to perform better on tasks specific to the chosen domain.

Finally, you will evaluate the fine-tuned model using the test dataset. They will generate predictions, calculate relevant evaluation metrics such as perplexity or BLEU scores, and assess how well the model performs compared to its pre-trained state. Optionally, you may compare their fine-tuned model's performance with that of API-based LLMs models. Through this assignment, you will gain practical skills in customizing LLMs for specific applications while understanding the nuances of dataset preparation, model training, and evaluation.
</p>

#### **Prerequisites**
- Familiarity with Python, PyTorch, and Unix command-line tools.
- Understanding of LLMs and transfer learning principles.
- Access to OpenAI or Ollama APIs for inference (optional for comparison).
- Access to GPU-enabled resources (e.g., dedicated GPU server, Google Colab, or Amazon SageMaker Studio).

---

### **Assignment Tasks**

#### **1. Dataset Preparation**
1. **Curate Training Data**:
   - Select a domain or topic of interest (e.g., legal documents, medical text, technical manuals, or conversational data).
   - Collect at least 10,000 lines of text data relevant to your chosen domain.
   - Preprocess the data by:
     - Removing unnecessary whitespace and special characters.
     - Tokenizing the text if required by the model architecture.

2. **Create a Test Set**:
   - Extract 10% of your curated data as a test set.
   - Ensure the test set is representative of your domain and does not overlap with the training data.

#### **2. Fine-Tuning the LLM**
1. Use the provided Python code template (see below) to fine-tune a pre-trained transformer-based LLM (e.g., GPT-2 or GPT-Neo) using PyTorch.
2. Modify the code to:
   - Load your curated training dataset.
   - Configure hyperparameters such as batch size, learning rate, and number of epochs.
3. Submit the fine-tuning job as a batch process on your GPU server.

#### **3. Model Evaluation**
1. Evaluate your fine-tuned model on the test set:
   - Generate predictions for each input in the test set.
   - Compare predictions against expected outputs (if applicable).
2. Calculate evaluation metrics such as:
   - Perplexity
   - BLEU score (for text generation tasks)
   - Any other relevant metric based on your use case.

3. Optionally, compare the performance of your fine-tuned model with an API-based LLM like OpenAI's GPT-4 or Ollama's models.

---

### **Provided Python Code Template**

Below is a basic PyTorch code template for fine-tuning an LLM:

```python
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments

# Step 1: Define Dataset Class
class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length=512):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )
        return encoding.input_ids.squeeze(), encoding.attention_mask.squeeze()

# Step 2: Load Pre-trained Model and Tokenizer
model_name = "gpt2"  # Replace with "EleutherAI/gpt-neo-125M" for GPT-Neo
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Step 3: Load and Preprocess Data
train_texts = ["Your training data here..."]  # Replace with actual data
test_texts = ["Your test data here..."]      # Replace with actual data

train_dataset = TextDataset(train_texts, tokenizer)
test_dataset = TextDataset(test_texts, tokenizer)

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=8)

# Step 4: Define Training Arguments
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=8,
    save_steps=500,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=100,
    evaluation_strategy="epoch",
    fp16=True  # Enable mixed precision for faster training on GPUs
)

# Step 5: Fine-Tune Model Using Trainer API
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer
)

trainer.train()

# Step 6: Save Fine-Tuned Model
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")
```

---

### Deliverables**
1. A report detailing:
   - The domain/topic chosen for fine-tuning.
   - The process of curating and preprocessing your dataset.
   - The hyperparameters used during fine-tuning.
   - Evaluation metrics and results on the test set.
   - Comparison with API-based LLMs (if applicable).
2. The fine-tuned model saved in a directory (`./fine_tuned_model`).
3. Python scripts or Jupyter notebooks used for:
   - Dataset preparation.
   - Fine-tuning process.
   - Model evaluation.

---

### Grading Criteria**
- **Dataset Quality (20%)**: Relevance and cleanliness of training/test datasets.
- **Code Implementation (30%)**: Correctness and modifications to the provided code template.
- **Model Performance (30%)**: Evaluation metrics and improvement over baseline performance.
- **Report Quality (20%)**: Clarity and completeness of explanations in the report.

---

### Additional Notes**
- Use Google Colab or SageMaker Studio if you do not have access to a dedicated GPU server.
- Feel free to experiment with different hyperparameters or models to improve performance.
- For any questions or issues during implementation, reach out via the course discussion forum.




### Questions to Consider

- How can you ensure their text data is diverse and representative for fine-tuning
- What are the best practices for splitting the dataset into training and test sets
- How can you monitor the progress of the batch job on the GPU server
- What metrics should you use to evaluate the performance of the fine-tuned model
- How can you handle potential biases in the text data during the fine-tuning process


### Use Cases

A concrete use case that demonstrates how domain-specific fine-tuning improves question-answering (QA) capabilities is found in the healthcare domain, particularly in medical QA systems. For example, fine-tuning pre-trained LLMs like LLaMA-2 or Mistral using advanced techniques such as rsDoRA+ and ReRAG has been shown to significantly enhance the accuracy and reliability of responses to medical questions. These fine-tuned models leverage domain-specific datasets, such as MediQA and Anki Flashcards, to better understand medical terminology, reasoning, and contextual accuracy. The fine-tuning process enables the models to provide precise answers to complex medical queries, aiding healthcare providers in making faster and more informed decisions. This approach not only improves the quality of information but also fosters greater patient trust by delivering dependable healthcare advice<a href="https://arxiv.org/html/2410.16088v1" target="_blank">[3]</a><a href="https://www.restack.io/p/fine-tuning-answer-llm-question-answering-cat-ai" target="_blank">[9]</a>.

Another compelling example is the use of fine-tuned LLMs for financial QA tasks. In a study involving the FinanceBench SEC filings dataset, fine-tuned models outperformed generic LLMs in accuracy when answering domain-specific questions. By combining a fine-tuned embedding model with a fine-tuned generative model in a Retrieval-Augmented Generation (RAG) pipeline, researchers observed substantial performance gains. This setup allowed the system to retrieve relevant financial data and synthesize accurate answers, achieving near human-expert quality. Such improvements are critical for applications like financial analysis, where precise and contextually relevant answers are essential<a href="https://arxiv.org/html/2404.11792v1" target="_blank">[7]</a>.

In both cases, domain-specific fine-tuning enables LLMs to overcome the limitations of generic models by adapting to specialized vocabulary, context, and reasoning patterns. This results in more accurate and reliable QA systems tailored to specific industries, demonstrating the transformative potential of fine-tuning for real-world applications.

## Citations
- [1] https://aisera.com/blog/fine-tuning-llms/
- [2] https://kili-technology.com/large-language-models-llms/the-ultimate-guide-to-fine-tuning-llms-2024
- [3] https://arxiv.org/html/2410.16088v1
- [4] https://kili-technology.com/large-language-models-llms/building-domain-specific-llms-examples-and-techniques
- [5] https://arxiv.org/html/2408.12247v2
- [6] https://solutyics.com/fine-tuning-a-language-model-for-question-answering-a-comprehensive-guide/
- [7] https://arxiv.org/html/2404.11792v1
- [8] https://genai.stackexchange.com/questions/1880/how-do-people-fine-tune-llms-to-only-answer-domain-specific-questions
- [9] https://www.restack.io/p/fine-tuning-answer-llm-question-answering-cat-ai
- [10] https://blog.gopenai.com/day-13-fine-tuning-llms-for-specific-use-cases-278c4535a468?gi=48d00f7f6b10
- [11] https://www.datacamp.com/tutorial/fine-tuning-large-language-models
- [12] https://www.linkedin.com/pulse/limits-domain-specific-fine-tuning-large-language-models-zixuan-liu-xs0if
- [13] https://www.superannotate.com/blog/llm-fine-tuning
- [14] https://arxiv.org/html/2401.09168v1
- [15] https://livebook.manning.com/book/ai-powered-search/chapter-14/v-20/
- [16] https://www.turing.com/resources/finetuning-large-language-models