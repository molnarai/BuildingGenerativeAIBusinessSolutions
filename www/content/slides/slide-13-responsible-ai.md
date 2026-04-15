+++
title = "Responsible AI"
description = "How to govern Agentic AI systems"
weight = 130
outputs = ["Reveal"]
math = true
thumbnail = "/imgs/slides/responsible_ai_3.png"

[reveal_hugo]
custom_theme = "css/reveal-robinson.css"
slide_number = true
transition = "none"

+++

{{< slide background-image="/imgs/slides/responsible_ai_3.png" >}}
<div style="min-height: 15em;"></div>
<div style="margin:0; padding: 50; background-color: rgba(0,0,0,0.5); min-hight:100%; min-width:100%" >
    <h1 style="color:white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);" >Responsible AI</h1>
    <p style="color:white; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);" > MSA 8700 — Module 13</p>
</div>

{{% note %}}


{{% /note %}}



***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_00.png" >}}
<h1></h1>

***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_01.png" >}}
<h1></h1>

***
### Core Principles

<p style="font-size: small; text-align: right">as established in the EU's Ethics Guidelines for Trustworthy AI
</p>

<div style="display: flex; flex-direction: column; gap: 12px; font-size: 0.55em;">

<div style="background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 12px 18px; text-align: left;">
<h3 style="margin:0 0 4px 0;">Beneficence</h3>
AI should actively benefit people and society — not merely avoid harm. The obligation is positive: to do good, not just to refrain from doing harm.
</div>

<div style="background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 12px 18px; text-align: left;">
<h3 style="margin:0 0 4px 0;">Non-maleficence</h3>
AI must not cause harm, including through inaction, unintended side effects, or emergent behavior. This is the classical medical principle "do no harm" extended to autonomous systems.
</div>

<div style="background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 12px 18px; text-align: left;">
<h3 style="margin:0 0 4px 0;">Autonomy</h3>
Respect for people's ability to understand, contest, and override AI decisions that affect them. This operationalizes as informed consent, explainability, and meaningful override mechanisms — the right not just to be informed but to actually exercise control.
</div>

<div style="background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 12px 18px; text-align: left;">
<h3 style="margin:0 0 4px 0;">Justice</h3>
The benefits and burdens of AI should be distributed fairly across groups and geographies. This covers both procedural justice (fair process) and distributive justice (fair outcomes) — and directly motivates bias and fairness requirements in system design.
</div>

<div style="background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 12px 18px; text-align: left;">
<h3 style="margin:0 0 4px 0;">Explicability</h3>
AI behavior must be understandable and auditable by the relevant stakeholders — at the appropriate level of abstraction for each audience. A patient, a clinician, and a regulator need different explanations of the same decision; all three are legitimate.
</div>

</div>

*** 

{{< slide content-image="/imgs/Engineering_Agentic_Governance_02.png" >}}
<h1></h1>

***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_03.png" >}}
<h1></h1>

***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_04.png" >}}
<h1></h1>

***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_05.png" >}}
<h1></h1>

***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_06.png" >}}
<h1></h1>

***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_07.png" >}}
<h1></h1>

***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_08.png" >}}
<h1></h1>

***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_09.png" >}}
<h1></h1>

***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_10.png" >}}
<h1></h1>

***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_11.png" >}}
<h1></h1>

***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_12.png" >}}
<h1></h1>

***

{{< slide content-image="/imgs/Engineering_Agentic_Governance_13.png" >}}
<h1></h1>

*** 

# Class Discussion

Open the discussion forum on iCollege

***

### Discussion Question 1
# Foundations of AI Ethics

An agentic AI system deployed in a hospital autonomously schedules and cancels patient appointments based on resource optimization. A patient misses a critical follow-up and suffers a worsening condition.

How do the five core ethical principles map onto this scenario, and which principle do you consider most violated?

***

### Discussion Question 2
# Bias &amp; Fairness

Your team is building a loan-decision agentic system for a regional bank. You discover that historical lending data reflects decades of discriminatory lending practices.

You have three options: (A) train on the data as-is, (B) remove protected attributes from features, or (C) apply fairness-aware re-weighting. What is your recommendation and why? What fairness metric would you use to validate it?

***

### Discussion Question 3
# Accountability &amp; Oversight

Building Agentic AI Business Solutions · Graduate Course · Session: Ethics &amp; Responsible AI in Agentic Systems 29 You are designing an agentic customer service system for a financial services firm. The system can autonomously resolve disputes, issue refunds up to $\$500$, and escalate to human agents.

A proposal is made to raise the autonomous refund threshold to $\$5,000$ to reduce human workload by 80%. What autonomy level would you recommend for this new threshold, and what safeguards would you require before approval?


***

### Discussion Question 4
# Governance

Your organization wants to deploy an agentic AI system that monitors employee communications (Slack, email, documents) to detect IP theft and policy violations. The system will flag suspicious behavior to HR.

What governance structures, consent mechanisms, and technical safeguards would you require before approving this deployment, and are there conditions under which you would refuse to build it?

*** 

### Discussion Question 5
# Synthesis

You have been hired as the AI Ethics Lead at a startup deploying a multi-agent system to autonomously manage a portfolio of real estate investments — identifying properties, negotiating purchase terms, managing tenants, and initiating legal proceedings when necessary.

Using any frameworks discussed today, identify the three most significant ethical risks and design one concrete mitigation for each. Would you take this job?

***