---
draft: false
title: RAG Simulator with AWS PartyRock
weight: 12
description: Demonstration of AWS PartyRock building and experimenting with a RAG Simulator
---

AWS PartRock is a free, no-code platform to experiment Generative AI. While the demonstration is not a functional RAG system, is shows some of its concepts.
<!-- more -->

{{<figure src="imgs/partyrock-welcome.png" width="800" alt="Figure 2" >}}

## Login to AWS PartyRock

1. Go to [AWS PartyRock](https://partyrock.aws/)
2. Click on "Get Started for Free"
3. Sign in with your Amazon account or create a new one
4. Once logged in, you will be directed to the PartyRock dashboard

Explore the tool, read the [PartyRock Guide](https://partyrock.aws/guide), click on "Generate app" and ask Whiskers, the AI chatbot, for help.

## RAG Pipeline Pipeline Demonstrator

Visit <https://partyrock.aws/u/peteratpartrock/Da-zp1w3M/MSA8700-RAG-Demonstrator>

This app demonstrates how Retrieval-Augmented Generation (RAG) works. RAG combines document retrieval with AI generation to provide accurate, context-aware answers. Follow the steps below to see each part of the RAG pipeline in action.

**Step-by-step RAG pipeline:**

- Document Upload - Users upload their own documents
- Chunking Demo - Shows how documents break into searchable pieces
- Embeddings Explanation - Explains how text converts to vectors (not actually functioning)
- Query Input - Users ask questions
- Retrieval Simulation - Shows which chunks would be found with relevance scores
- RAG Response - Generates an answer using only retrieved context
- Chat Interface - For follow-up questions and deeper exploration

The app walks through the entire RAG process visually, so users understand how retrieval-augmented generation actually works. Try uploading a document and asking questions to see it in action!

{{<figure src="imgs/partyrock-rag-demonstrator-top.png" width="800" alt="Figure 1" >}}
{{<figure src="imgs/partyrock-rag-demonstrator-bottom.png" width="800" alt="Figure 2" >}}


**Try these files** (only upload a single file, and delete for the next):
- [rag-survey-paper-2409.14924v1.pdf](https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/aux/rag-survey-paper-2409.14924v1.pdf) a paper on RAG systems. Example questions:
    - *"What a the key components of a RAG?"*
    - *"Explain the difference between Level 3 and Level 4 queries?"*
    - *"Explain the difference sparse and dense retrieval methods?"*
- [Catalog7000RobinsonCollegeOfBusiness.docx](https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/aux/Catalog7000RobinsonCollegeOfBusiness.docx) an exerpt of GSU Catalog about the Robinson College of Business. Example questions:
    - *"Where is the dean's office located?"*
    - *"List the academic units and centers."*
    - *"Can I join a study abroad program in Hungary?"*
- [InsightLabProjects2.md](https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/aux/InsightLabProjects2.md) an overview of industry projects at the Institute for Insight. Example questions:
    - *"Which companies sponsored LLM focussed projects?"*
    - *"Were there any projects related to image processing or computer vision?"*
    - *"Were there any healthcare related projects?"*

Use the edit function to explore how the application works.

