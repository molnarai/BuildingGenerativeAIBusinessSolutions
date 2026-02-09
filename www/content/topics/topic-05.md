---
date: 2026-02-16
classdates: 'Monday 2026-02-16, Wednesday 2026-02-11'
draft: false
title: 'Agent Systems'
weight: 50
numsession: 5
---
The session frames agentic AI as an evolution of basic RAG for business workflows. It starts by contrasting a static RAG pipeline—query, retrieve, answer—with an AI agent that interprets goals, plans multi-step processes, chooses among tools (including RAG), and iterates based on feedback until the goal is satisfied.
<!--more-->

<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/From_Prompt_Engineering_to_Flow_Engineering.m4a" type="audio/mp4" />
    Your browser does not support the audio element.
</audio>


Core agent components appear as a loop: a foundation model for reasoning and decisions, planning and control logic to break goals into subtasks, tool interfaces to external systems and RAG, memory for context and history, explicit state and policies expressing constraints, and observation/feedback to evaluate tool outputs and decide when to retry, adjust, or escalate. A customer support example shows how an agent not only explains refund policy but also verifies accounts, calls CRM and billing APIs, applies rules, and coordinates the end-to-end resolution.

The discussion then extends to multi-agent systems, where specialized agents play distinct roles such as Planner, Retriever, Domain Expert, Generator, and Executor. An orchestrator coordinates which agent runs when, based on shared state, using either a fixed or adaptive pattern, while a shared memory/blackboard and coordination policies govern hand-offs, conflict resolution, and stopping conditions. A contract analysis and negotiation scenario illustrates this: planner for task decomposition, extractor for clause parsing, risk analyst using RAG over internal policy, drafter for redlines, and executor for integration with enterprise systems and human review. The overall narrative shifts the perspective from single-pass Q&A toward goal-directed, tool-using, and orchestrated systems for complex business processes.


## Readings
- [AI Agents in Action](https://learning.oreilly.com/library/view/ai-agents-in/9781633436343/) by Micheal Lanham, Manning Publications, February 2025
- [Building Applications with AI Agents](https://learning.oreilly.com/library/view/building-applications-with/9781098176495/) by Michael Albada, O'Reilly Media, Inc., September 2025
- [Building Generative AI Agents: Using LangGraph, AutoGen, and CrewAI](https://learning.oreilly.com/library/view/building-generative-ai/9798868811340/) by Tom Taulli, Gaurav Deshmukh, Apress, May 2025
- [Building AI Agents with LLMs, RAG, and Knowledge Graphs](https://learning.oreilly.com/library/view/building-ai-agents/9781835087060/) by Salvatore Raieli, Gabriele Iuculano, Packt Publishing, July 2025