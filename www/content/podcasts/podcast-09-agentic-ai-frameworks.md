---
title: Agentic AI frameworks
subtitle: Agentic AI frameworks are transforming the development of intelligent systems by integrating Large Language Models (LLMs) with traditional programming languages to create autonomous agents capable of complex decision-making and task execution.
author: [Your Name]
date: 2025-03-24
tags: [user experience design, skills, orchestration, multi-agent systems]
---
**Detailed Timeline of Main Events Covered in the Sources:**

**Early Stages of Agentic Systems (Implied Throughout)**

- Development of early text-based agent interfaces.
- Introduction and evolution of graphical user interfaces for agent interaction.
- Challenges with latency in early speech and voice interfaces due to processing limitations.

**Recent Advancements (Ongoing)**

- Significant advancements in low-latency speech recognition models.
- Development of more efficient language processing architectures, reducing delays in voice interactions.
- Increased accessibility and ease of deployment of text-based agents.

**Development of Agent Skills (Chapter 4 Focus)**

- Concept of "skills" as modular components enabling agents to perform tasks and make decisions.
- Skills range from simple, single-step tasks to complex, multi-step operations.
- Emphasis on hand-crafted skills for areas like calculator operations, calendar changes, and map/graph manipulation to improve efficacy.
- Introduction of tools within code (using Langchain as an example) to define agent capabilities (e.g., multiply, exponentiate, add).
- Demonstration of binding tools to Language Model Models (LLMs) like GPT-4o, allowing the LLM to choose and invoke tools to answer queries.
- Examples of creating skills for web browsing (using Wikipedia API) and accessing external APIs (simulated stock price retrieval).
- Discussion of plugin skills offered by platforms like Google's Gemini and Microsoft's Phi, expanding agent functionalities (image recognition, speech synthesis, etc.).
- Active contribution of new plugin skills and enhancements by the open-source AI community (e.g., on GitHub).
- Considerations for effective skill design, including granularity (decomposing complex tasks) and semantic collision avoidance through hierarchical grouping of related skills.
- Exploration of skill learning from rewards using value-based (Q-learning, DQNs) and policy-based (REINFORCE) methods.

**Orchestration of Agent Skills (Chapter 5 Focus)**

- Focus on orchestration, including skill selection, execution, skill topologies, and planning.
    - Skill Selection: Generative Skill Selection: LLM directly determines which skill to use based on the query.
    - Semantic Skill Selection: Embedding skill descriptions and the user query in a vector space and using similarity search to select relevant skills (recommended for most use cases).
    - Implementation details of Semantic Skill Selection, including embedding models (OpenAI's ada, Amazon's Titan, etc.), vector databases (FAISS), and the process of embedding, indexing, searching, and parameterizing skills.
    - Hierarchical Skill Selection: Grouping skills and selecting a relevant group first, then selecting a specific skill within that group, for scenarios with a large number of skills.
    - Mention of fine-tuning smaller models for skill selection as an alternative but with maintenance considerations.
- Parametrization: Defining and setting parameters for skill execution, leveraging the current agent state and potentially external context (time, location).
- Skill Execution: Locally executing some skills, while others are executed remotely via APIs.
    - Skill Topologies: Single Skill Execution: Tasks requiring only one skill.
    - Parallel Skill Execution: Executing multiple skills concurrently and combining their results.
    - Chains (Linear): Sequential execution of skills where the output of one feeds into the next.
    - Trees (Hierarchical): Branching execution paths with decision points.
    - Graphs (Interconnected Networks): Complex, nonlinear dependencies between skills.
    - Planning: Iterative Planning: Choosing and executing one action at a time ("unplanned" or "greedy" approach).
    - Zero-Shot Planning: Generating a plan for a task before execution, based on understanding of the task and environment.
    - Refinement Planning: Starting with an initial plan and iteratively adjusting it based on execution outcomes or new information.

**Moving to Multi-Agent Systems (Chapter 7 Focus)**

- Transitioning from single-agent to multi-agent systems to enhance the ability to solve complex tasks.
- Determining the optimal number of agents based on task complexity, environment, and agent interactions.
- Single-Agent Scenarios: Suitable for simple, well-defined, or isolated tasks.
- Benefits of Multi-Agent Systems:Handling complex and diverse tasks.
- Parallel processing capabilities.
- Enhanced fault tolerance through redundancy.
- Adaptability to changing conditions.
- Increased robustness.
- Multi-Agent Coordination Strategies: 
    - Democratic Coordination: Equal decision-making power and consensus.
    - Manager Coordination: Centralized control with designated managers.
    - Hierarchical Coordination: Layered structure with distributed responsibilities.
    - Actor-Critic: One agent makes decisions (actor), another provides feedback (critic) for learning.
    - Self-Organizing: Agents autonomously interact and coordinate based on local rules.
- Autonomous Design of Agentic Systems (ADAS): A meta-agent automatically creates, assesses, and refines other agents through code, using a Meta Agent Search (MAS) algorithm with an iterative cycle of generation, evaluation, and archiving.
- Multi-Agent Frameworks: 
    - Do-It-Yourself (DIY): Building a system tailored to specific needs.
    - Langchain: A framework offering tools and abstractions for building agentic applications, including multi-agent capabilities (e.g., AgentExecutor, SequentialChain, RouterChain, Swarm).
    - Swarm: A high-level API within Langchain for orchestrating multiple agents in a conversational setting, handling function execution, handoffs, and context.

**Principles for Effective Agent Design (Chapter 3 Implied Throughout)**

- Importance of understanding user experience (UX) principles for agentic systems.
- Various interaction modalities between agents and users (text, graphical interfaces, speech, video).
- Strengths and limitations of different modalities (e.g., text for clarity, graphics for visual richness, voice for hands-free).
- Crucial role of context retention (short-term and long-term memory) for seamless interactions.
- Challenges of data persistence in context management.
Importance of clear communication about agent capabilities, limitations, and operational context to build trust.
- Setting realistic expectations upfront about what an agent can and cannot do.
- Communicating confidence and uncertainty effectively (explicit statements, visual cues, behavioral adjustments).
- Knowing when to ask for help through clear, polite, and context-aware questions.
- Handling failure gracefully by acknowledging issues, explaining why, and providing alternative options.
- The power of transparency and predictability in building and maintaining user trust.
- Ensuring consistency in agent behavior and responses.
- Preventing automation bias by encouraging user engagement and critical thinking.

**Cast of Characters with Brief Bios:**

- Agent Systems (Generic): Intelligent software entities designed to perceive their environment and take actions to achieve specific goals. They interact with users through various modalities and utilize skills to perform tasks.

- Users (Generic): Individuals who interact with agent systems to accomplish tasks or obtain information. Their trust and effective collaboration are key to successful agentic applications.

- AI Agents (Generic): A specific type of agent system powered by artificial intelligence, capable of learning, reasoning, and problem-solving to varying degrees.

- Large Language Models (LLMs) (e.g., GPT-4o): Foundation models trained on vast amounts of text data, enabling them to understand and generate human-like language. They form the core intelligence of many agentic systems, capable of reasoning, planning, and utilizing tools.

- Meta-Agent (in ADAS): A higher-level agent responsible for automatically designing, evaluating, and refining other agentic systems through code.

- Actor (in Actor-Critic Coordination): An agent within a multi-agent system that makes decisions and takes actions.

- Critic (in Actor-Critic Coordination): An agent within a multi-agent system that evaluates the actions of the actor and provides feedback to improve performance.

- Shengran Hu, Cong Lu, and Jeff Clune: Researchers who articulated the concept of Autonomous Design of Agentic Systems (ADAS).

- sevans@oreilly.com: The editor at O'Reilly Media mentioned for reader feedback on the book.

- Buzz Aldrin: Mentioned as an example in the context of a Wikipedia search skill. An American former astronaut and pilot of the Lunar Module Eagle on Apollo 11, the first crewed landing on the Moon.

<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Agentic_AI_frameworks.wav" type="audio/wav">
    Your browser does not support the audio element.
</audio>

| Speaker | Transcript |
| ------- | ---------- |
