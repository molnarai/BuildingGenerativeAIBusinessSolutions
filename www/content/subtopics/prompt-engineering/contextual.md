---
title: Contextual Prompting
weight: 40
description: Contextual Prompting is a technique where additional context is strategically incorporated into the input prompt to guide the model's response toward a desired outcome. 
---
Contextual Prompting is a technique where additional context is strategically incorporated into the input prompt to guide the model's response toward a desired outcome. This context can include background information, examples, or clarifying details that frame the task more effectively. By tailoring the input to provide relevant cues, Contextual Prompting enhances the model's understanding of the task and reduces ambiguity, improving performance on tasks such as question answering, text generation, and classification.

<!-- more -->
Here are three detailed examples of **Contextual Prompting**, ranging from simple to complex:

---

### 1. **Simple Example: Writing a Historical Question**
   - **Task**: Generate a multiple-choice question about the Renaissance.
   - **Prompt**:
     ```
     Context: Suppose you are a history teacher with more than 30 years of teaching experience.

     Instructions: Write a multiple-choice question for a history course.

     Relevance: The question should be related to the Renaissance.

     Constraint: There should be more than two correct answers among the four options.
     ```
   - **Output**:
     ```
     Question: Which of the following were significant contributions of the Renaissance period?
     A. Development of perspective in art
     B. Invention of the printing press
     C. Discovery of antibiotics
     D. Revival of classical learning

     Correct Answers: A, B, D
     ```
   - **Explanation**: By providing background (teacher role), relevance (Renaissance), and constraints (multiple correct answers), the AI is guided to generate an accurate and contextually relevant response<a href="https://github.com/EgoAlpha/prompt-in-context-learning/blob/main/PromptEngineering.md" target="_blank">[1]</a>.

---

### 2. **Intermediate Example: Customer Support Chat**
   - **Task**: Respond to a customer complaint about delayed shipping.
   - **Prompt**:
     ```
     Context: You are an AI customer support agent for an e-commerce platform specializing in electronics. The customer has complained about a delayed shipment for their laptop.

     Instructions: Apologize, explain why the delay occurred, and offer a solution.

     Tone: Empathetic and professional.
     ```
   - **Output**:
     ```
     "Dear Customer,

     We sincerely apologize for the delay in shipping your laptop. Due to unexpected disruptions in our supply chain, your order was delayed. We understand how important this is to you and regret any inconvenience caused.

     As a resolution, we have expedited your shipment, which will now arrive within two business days. Additionally, we’re offering you a $20 voucher for your next purchase as an apology.

     Thank you for your patience and understanding.

     Best regards,
     Customer Support Team"
     ```
   - **Explanation**: The context ensures the AI understands the situation (delayed shipment) and adopts an appropriate tone while following clear instructions to craft a professional response<a href="https://www.acorn.io/resources/learning-center/prompt-engineering-examples/" target="_blank">[2]</a><a href="https://www.linkedin.com/pulse/725-contextual-prompting-enhancing-ai-background-knowledge-raj-vrtgc" target="_blank">[5]</a>.

---

### 3. **Complex Example: Scientific Explanation with Role-Specific Context**
   - **Task**: Explain black holes in a technical manner for an advanced physics student.
   - **Prompt**:
     ```
     Context: You are an AI research assistant specializing in astrophysics with expertise in black hole physics.

     Instructions: Provide a detailed explanation of how black holes are formed, suitable for an advanced physics student.

     Tone: Technical and scientific.
     ```
   - **Output**:
     ```
     "Black holes form when massive stars exhaust their nuclear fuel and undergo gravitational collapse. During this process, the outward pressure from nuclear fusion can no longer counteract gravitational forces. If the remnant core exceeds the Tolman–Oppenheimer–Volkoff limit (approximately 2-3 solar masses), it collapses into a singularity—a point of infinite density surrounded by an event horizon, beyond which nothing can escape.

     Black holes can also form through other mechanisms such as the merger of neutron stars or direct collapse during galaxy formation. Their properties are described by solutions to Einstein's field equations, such as the Schwarzschild or Kerr metrics."
     ```
   - **Explanation**: The prompt provides specialized context (AI as an astrophysics assistant) and specifies tone and audience level (advanced student), enabling the AI to generate a precise and technical explanation<a href="https://www.promptingguide.ai/introduction/examples" target="_blank">[3]</a><a href="https://www.godofprompt.ai/blog/what-is-context-in-prompt-engineering" target="_blank">[4]</a>.

---

These examples demonstrate how contextual prompting can guide AI to produce relevant, accurate, and tailored outputs by providing background information, constraints, tone specifications, and intended audience details.

## Citations
- [1] https://github.com/EgoAlpha/prompt-in-context-learning/blob/main/PromptEngineering.md
- [2] https://www.acorn.io/resources/learning-center/prompt-engineering-examples/
- [3] https://www.promptingguide.ai/introduction/examples
- [4] https://www.godofprompt.ai/blog/what-is-context-in-prompt-engineering
- [5] https://www.linkedin.com/pulse/725-contextual-prompting-enhancing-ai-background-knowledge-raj-vrtgc