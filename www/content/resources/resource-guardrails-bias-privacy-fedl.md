---
draft: false
title: Safeguarding LLMs, Detecting BIAS, Privacy, Federated Learning
weight: 50
description: Below are various resources related to Safeguarding LLMs, Detecting BIAS, Privacy, Federated Learning.
---

**Synopsis:**

**Safeguarding LLMs, Detecting BIAS, Privacy, Federated Learning**

The distinct architectures and accessibility models of open versus closed source Large Language Models (LLMs) have significant implications for privacy considerations and potential vulnerabilities.
Open Source LLMs:

Architecture and Accessibility: Open source LLMs are publicly accessible, meaning their underlying architecture and parameters can be examined, modified, and shared by the community. This transparency allows for greater scrutiny of the model's workings.

Privacy Considerations:

Transparency: The accessibility of open source LLMs can be advantageous for privacy as researchers and the community can analyze the model for potential privacy vulnerabilities, biases in training data, and data handling practices. This scrutiny can lead to the identification and mitigation of privacy risks.

Customization: Users have the freedom to fine-tune and adapt open source LLMs for specific tasks. This could allow for the implementation of privacy-enhancing techniques or the removal of potentially problematic aspects of the model.

Security Responsibility: However, the responsibility for addressing security vulnerabilities (Common Vulnerabilities and Exposures, or CVEs) in the underlying software versions often falls on the users themselves. This means that if users do not have the expertise or resources to manage these vulnerabilities, they could be exposed to privacy risks.

Potential Vulnerabilities: While the open nature can aid in identifying vulnerabilities, the accessibility of the architecture might also provide attackers with more information to craft targeted privacy attacks, such as prompt injection attacks or attempts to extract training data. The need for users to manage security updates also presents a potential vulnerability if not handled properly.
Closed Source LLMs:

Architecture and Accessibility: Closed source LLMs are developed and owned by specific organizations, and their architecture and parameters are not publicly disclosed. This lack of transparency means users have limited insight into how these models function.

Privacy Considerations:

Limited Transparency: The proprietary nature of closed source LLMs means users have limited visibility into their data handling practices, training data, and security measures. This can raise privacy concerns as users must trust the developers to uphold privacy standards.

Vendor Responsibility: The developers of closed source LLMs retain control over their models and are responsible for addressing security vulnerabilities. This can be beneficial for users who may lack the technical expertise to secure open source models themselves. However, the "black box" nature means users have to rely on the vendor's diligence in identifying and fixing issues.

Data Policy: The data policy of closed source LLM providers, such as the use of data for model training unless users explicitly opt out, can also have privacy implications, as illustrated by the Samsung incident where sensitive data shared with ChatGPT became potentially accessible for model refinement.

Potential Vulnerabilities: While the internal workings are not public, closed source LLMs are still susceptible to various privacy attacks such as prompt injection, which could potentially lead to the disclosure of sensitive information if the training data contained such information. Real-world incidents, like the Samsung data leaks to ChatGPT, highlight the risk of sensitive information disclosure when using closed source LLMs, even if inadvertently. Users have less control over mitigating these risks directly compared to open source models.

In summary, open source LLMs offer greater transparency and customization for privacy but place the responsibility for security on the user, while closed source LLMs provide security management by the vendor but lack transparency and user control over privacy aspects. Both types of LLMs face potential privacy vulnerabilities like prompt injection and the risk of sensitive data exposure, necessitating careful consideration of data handling practices and security measures.

**Texts:**

1. Textbooks: 
    - [Chapter 12. Responsible AI](https://go.oreilly.com/georgia-state-university/library/view/building-llm-powered/9781835462317/Text/Chapter_12.xhtml#_idParaDest-168) in Valentina Alto, "Building LLM Powered Applications", O'Reilly Media Inc., Published by Packt Publishing. This book is available in print and digital on O’Reilly Media.

    - [Chapter 1. Introduction](https://go.oreilly.com/georgia-state-university/library/view/privacy-and-security/9781098160838/ch01.html#id18) in Baihan Lin, "Privacy and Security for Large Language Models", O'Reilly Media Inc., Published by Packt Publishing. This book is available in print and digital on O’Reilly Media.

    - [Chapter 3. Navigating the Cultural, Social, and Legal Landscapes](https://go.oreilly.com/georgia-state-university/library/view/privacy-and-security/9781098160838/ch03.html#id46) in Baihan Lin, "Privacy and Security for Large Language Models", O'Reilly Media Inc. Published by Packt Publishing. This book is available in print and digital on O’Reilly Media.

    - [Chapter 3. Architectures and Trust Boundaries](https://go.oreilly.com/georgia-state-university/library/view/the-developers-playbook/9781098162191/ch03.html) in Steve Wilson, "The Developer's Playbook for Large Language Model Security", O'Reilly Media Inc. This book is available in print and digital on O’Reilly Media.

    - [Chapter 12. A Practical Framework for Responsible AI Security](https://go.oreilly.com/georgia-state-university/library/view//the-developers-playbook/9781098162191/ch12.html) in Steve Wilson, "The Developer's Playbook for Large Language Model Security", O'Reilly Media Inc. This book is available in print and digital on O’Reilly Media.

2. Articles:     
    - Bijit Ghosh, **LLM Privacy and Security** <br /> [Link](https://medium.com/@bijit211987/llm-privacy-and-security-56a859cbd1cb)
    
    - Sanjay K Mohindroo, **Data Privacy and Compliance for Large Language Models (LLMs)** <br /> [Link](https://medium.com/@sanjay.mohindroo66/data-privacy-and-compliance-for-large-language-models-llms-37d8179ac12b)

    - Skanda Vivek, **Privacy In Large Language Models** <br /> [Link](https://medium.com/emalpha/privacy-in-large-language-models-498cacb5d1bb)

    - Sulbha Jain, **Responsible AI: Measuring and Explaining LLM’s Fairness and Bias** <br /> [Link](https://medium.com/@sulbha.jindal/responsible-ai-measuring-and-explaining-llms-fairness-and-bias-9b5196dd6222)

    - Shuchismita Sahu, **What Are Guardrails for LLMs?s** <br /> [Link](https://ssahuupgrad-93226.medium.com/llm-guardrails-f025e5d8111b)

    - Jeffrey Ip, **LLM Guardrails for Data Leakage, Prompt Injection, and More** <br /> [Link](https://www.confident-ai.com/blog/llm-guardrails-the-ultimate-guide-to-safeguard-llm-systems)

    - Chia Jeng Yang, **Rules, Extraction Guardrails, Knowledge Table & KG Studio** <br /> [Link](https://medium.com/enterprise-rag/rules-extraction-guardrails-knowledge-table-studio-e84999ade353)

    - Nachi Keta, **Guardrails for Enterprise Specific LLMs — A Cursory Survey** <br /> [Link](https://nachi-keta.medium.com/guardrails-for-enterprise-specific-llms-a-cursory-survey-89df959aaa21)

    - Rohan Rao, Benika Hall, Sunil Patel, Christopher Brissette, and Gordana Neskovic, **Insights, Techniques, and Evaluation for LLM-Driven Knowledge Graphs** <br /> [Link](https://developer.nvidia.com/blog/insights-techniques-and-evaluation-for-llm-driven-knowledge-graphs/)

    - Suriya Ganesh Ayyamperumal, Limin Ge, **Current state of LLM Risks and AI Guardrails**, <br /> [Link](https://www.researchgate.net/publication/381580070_Current_state_of_LLM_Risks_and_AI_Guardrails)

3. Paper: Yi Dong, Ronghui Mu, Gaojie Jin, Yi Qi, Jinwei Hu, Xingyu Zhao, Jie Meng, Wenjie Ruan, Xiaowei Huang, [Building Guardrails for Large Language Models](https://arxiv.org/abs/2402.01822v1)[PDF]
