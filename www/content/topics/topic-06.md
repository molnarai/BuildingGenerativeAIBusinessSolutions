---
date: 2026-02-23
classdates: 'Monday 2026-02-23, Wednesday 2026-02-18'
draft: false
title: 'Agentic Frameworks'
weight: 60
numsession: 6
---
This session evaluates leading Python-based agentic AI frameworks. The guide highlights LangGraph, Microsoft AutoGen, Strands Agents, and LlamaIndex as the most durable and pedagogically distinct tools for building intelligent systems. These frameworks are categorized into four schools of thought: graph-based workflows, multi-agent conversations, model-driven orchestration, and data-centric retrieval. Furthermore, the sources compare how these libraries implement core agent functions like memory, perception, and reasoning. The material also contrasts these code-first Python SDKs with visual automation platforms like n8n, while emphasizing emerging interoperability standards such as MCP and A2A.
<!--more-->

{{< podcast src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/the_four_philosophies_of_agentic_ai.m4a" title="The Four Philosophies of Agentic AI" >}}



### Python Fameworks
{{<figure src="imgs/Python_Agent_Architectures_Compared001.png" width="100%" alt="Four Python Frameworks" >}}

1. **LangChain / LangGraph** <https://www.langchain.com/langgraph>
    - **Role in lecture:** The “full‑stack, general‑purpose” baseline.
    - **Why it’s essential:** Broadest ecosystem, tooling, RAG, and strongly opinionated workflows; LangGraph now serves as the de facto standard for **stateful, graph‑based, multi‑step agents**. Frequently cited as the center of the Python agentic landscape.


2. **Microsoft AutoGen** <https://microsoft.github.io/autogen/stable//index.html>
    - **Role in lecture:** **Multi‑agent conversation and orchestration.**
    - **Why it’s essential:** Focuses on agent‑to‑agent collaboration, self‑reflection, and human‑in‑the‑loop workflows. Frequently listed among the top agentic frameworks for production‑grade multi‑agent systems.


3. **Strands Agents** <https://strandsagents.com/latest/>
    - **Role in lecture:** **Model‑first, observable, production‑grade SDK.**
    - **Why it’s essential:** Lightweight, model‑agnostic, and explicitly designed for observable, tool‑driven agents, with strong AWS‑style telemetry and multi‑model support. Often highlighted as a good fit for production‑like, provider‑flexible agents and is mentioned in side‑by‑side comparisons alongside LangGraph, AutoGen, and Pydantic‑based frameworks.


4. **LlamaIndex (Agents)** <https://developers.llamaindex.ai/python/framework/>
    - **Role in lecture:** **Data‑centric and retrieval‑driven agents.**
    - **Why it’s worth adding:** LlamaIndex is increasingly treated as a first‑class “agent framework” layer atop its RAG infrastructure, with built‑in agent modes and tools for interacting with structured/unstructured data. It’s consistently ranked among the top agentic frameworks for data‑heavy, knowledge‑agent applications.

### No/Low-Code Famework
5. **N8N AI** <https://n8n.io/>
    - **Role in lecture:** **Visual, workflow‑centric agent orchestration.**
    - **Why it’s worth mentioning:** n8n is a source‑available automation platform that adds AI agent nodes to its drag‑and‑drop workflow builder, making it easy to connect LLM‑based agents with hundreds of existing SaaS and data integrations. It excels at production‑ready orchestration of clearly defined, event‑driven workflows (email, CRM, ticketing, data pipelines), where agents act as steps in a larger business process. Compared to Python‑native frameworks, n8n focuses less on deeply autonomous, stateful agents and more on **tying agents, tools, and traditional automation together** in a visual environment, including multi‑agent patterns where an orchestrator agent calls specialized sub‑agents and MCP‑based tools.



### Code Examples:
- [Examples of Agentic Frameworks](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/tree/main/AgenticAI/agentic-framework-examples) Agentic RAG with simple text document as knowledge source (LangGraph, Strands, AutoGen, LlamaIndex)
- [Examples of n8n](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/tree/main/N8N-Examples) 
Demonstration of using n8n built-in AI Agent
