---
date: 2026-01-12
classdates: 'Monday 2026-01-12, Wednesday 2026-01-14'
draft: false
title: 'AI Foundations'
weight: 10
numsession: 1
---
The topics in this session include foundational elements of logic and its application in AI (specifically Horn clauses and SLD resolution), different knowledge representation schemes (production rules, frames, and literals), methods for generalization and learning within these schemes (LGG, attribute-only space search, heuristic learning, and knowledge acquisition), and approaches to handling uncertainty in expert systems. Examples from various problem domains, such as mass spectrometry, symbolic integration, chemistry, music analysis, and student modeling, illustrate the practical application of these concepts.

<!-- more -->

Slide deck posted on the [iCollege](https://icollege.gsu.edu/) class site.

<audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/Symbolic_Artificial_Intelligence.m4a" type="audio/mp4" />
    Your browser does not support the audio element.
</audio>

## Reading
- Textbook: [Artificial Intelligence A New Synthesis](https://learning.oreilly.com/library/view/artificial-intelligence/9781558604674/) by Nils J. Nilsson, 1998.
- Textbook: [Machine Learning - An Artificial Intellegence Approach](https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/docs/Machine+Learning_+An+Artificial+Intelligence+Approach+(+PDFDrive+).pdf) edited by R. S. Michalski and J. G. Carbonell T. M. Mitchell, 1984.
- Paper: [Inductive Logic Programming At 30: A New Introduction](https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/docs/Inductive+logic+programming+at+30.pdf) by Andrew Cropper and Sebastijan Dumančić, 2022.
- Textbook: [Principles of Expert Systems](https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/docs/Principles+of+Expert+Systems.pdf) by Peter J.F. Lucas and Linda C. van der Gaag, 1991.


## Other Resource
- [Web-based Prolog Environment](https://swish.swi-prolog.org/)


### Formal Logic as a Foundation for AI:
The sources highlight the critical role of formal logic, particularly first-order predicate logic, as a rigorous basis for representing knowledge and performing inference in AI systems.
- Key Fact: Logic provides a well-defined syntax and semantics for expressing statements and relationships. Concepts like atomic formulas, terms, predicates, functions, variables, and constants are fundamental building blocks.
- Important Idea: Equivalence of formulas is a core concept, allowing for manipulation and simplification of logical expressions while preserving their truth values. De Morgan's laws and implications are cited examples of such equivalences.- Important Idea: Converting logical formulas into Clausal Form (conjunctive normal form) is a crucial step for applying automated reasoning techniques like resolution. This involves eliminating implications, reducing the scope of negations, standardizing variables, and eliminating quantifiers.
- Quote: "An atomic formula, or atom for short, is an expression of the form P (t1, . . . , tn), where P is an n-place predicate symbol, n ≥ 0, and t1, . . . , tn are terms." (Principles of Expert Systems.pdf)
- Quote: "A clause is a closed formula of the form ∀x1 · · · ∀xs(L1 ∨ · · · ∨ Lm) where each Li, i = 1, . . . ,m, m ≥ 0, is a literal..." (Principles of Expert Systems.pdf)

### Horn Clauses and SLD Resolution:
A significant focus is placed on Horn clauses as a restricted but powerful form of clauses, particularly relevant to logic programming languages like PROLOG.
- Key Fact: A Horn clause contains at most one positive literal. This includes unit clauses (a single positive literal) and goal clauses (only negative literals).
- Quote: "A Horn clause is a clause having one of the following forms: (1) A← (2) ← B1, . . . , Bn, n ≥ 1 (3) A← B1, . . . , Bn, n ≥ 1" (Principles of Expert Systems.pdf)
- Important Idea: SLD (Selective Linear Definite clause) resolution is a specific, efficient proof strategy for Horn clauses, forming the basis for PROLOG's execution model. It involves resolving a goal clause with a definite clause (a Horn clause with exactly one positive literal), selecting an atom in the goal, and using unification to find a most general unifier.
- Quote: "An SLD derivation is a finite or infinite sequence G0, G1, . . . of goal clauses, a sequence C1, C2, . . . of variants of input clauses and a sequence θ1, θ2, . . . of most general unifiers, such that each Gi+1 is derived from Gi =← A1, . . . , Ak and Ci+1 using θi+1 if the following conditions hold..." (Principles of Expert Systems.pdf)
- Important Idea: Unification is the core process in resolution (including SLD resolution) that finds a substitution to make two expressions identical. The Most General Unifier (MGU) is the most general such substitution. Renaming variables is crucial for correct unification.
- Quote: "A unifier θ of a unifiable set of expressions E = {E1, . . . , Em}, m ≥ 2, is said to be a most general unifier (mgu) if for each unifier σ of E there exists a substitution λ such that σ = θλ." (Principles of Expert Systems.pdf)
- Important Idea: Structure sharing, where variable bindings are stored in an environment rather than physically creating new clauses, is a common implementation technique for SLD resolution (mentioned in the context of LISP implementation).
- Quote: "The variable bindings created during resolution are stored in a data structure which is called an environment." (Principles of Expert Systems.pdf)

### Production Rules and Inference Systems:
Production rules (if-then rules) are presented as a common knowledge representation formalism, particularly in expert systems.
- Key Fact: A production rule consists of an antecedent (conditions) and a consequent (actions or conclusions).
- Quote: "A production rule is a statement having the following form: 〈production rule〉 ::= if 〈antecedent〉 then 〈consequent〉 fi" (Principles of Expert Systems.pdf)
- Important Idea: Production rules can be related to logical implications, where the antecedent is a conjunction of conditions (potentially involving disjunctions) and the consequent is a conjunction of actions/conclusions. The translation from production rules to ground logical implications is described.
- Quote: "Further translation of a production rule into a logical formula is now straightforward. The general translation scheme is as follows: if c1,1 or c1,2 or . . . or c1,m and . . . . . . cn,1 or cn,2 or . . . or cn,p then a1 also a2 also . . . also aq fi" (Principles of Expert Systems.pdf)
- Important Idea: Inference in production systems can be either top-down (goal-directed, backward chaining) or bottom-up (data-driven, forward chaining). Examples of rules and their application in a system like DPS (likely a variant of OPS) and IPS are provided, illustrating conditions matching elements in a working memory (WM) and actions asserting new data or goals.
- Quote: "A rule (that is, a production) in DPS consists of a number of conditions and a number of actions." (Machine Learning_ An Artificial Intelligence Approach ( PDFDrive ).pdf)
- Quote: "A method in IPS is a set of rules that work together to satisfy a goal." (Machine Learning_ An Artificial Intelligence Approach ( PDFDrive ).pdf)
- Important Idea: Patterns and facts are central to rule matching. Patterns can contain variables (single or multi-valued), while facts are concrete instances without variables. Matching involves finding substitutions for pattern variables that make the pattern identical to a fact.
- Quote: "A fact is a finite, ordered sequence of elements... where each element fi... is a constant." (Principles of Expert Systems.pdf)
- Quote: "The pattern variables occurring in a pattern may be replaced by one or more constants depending on the type of the variable..." (Principles of Expert Systems.pdf)

### Frames and Inheritance:
Frames and semantic nets are introduced as alternative knowledge representation paradigms, emphasizing structured knowledge about objects and their relationships.
- Key Fact: Semantic nets use vertices (nodes) to represent objects/concepts and labelled arcs (links) to represent relationships between them.
- Important Idea: Inheritance is a key mechanism in frame-based systems, allowing subclasses to inherit properties (attribute values) from their superclasses. Both single (tree-shaped taxonomies) and multiple (graph-shaped taxonomies) inheritance are discussed.
- Quote: "For each pair (y1, y2) ∈ ≤ we have y1 ≤ y2 ∈ ΩT." (Principles of Expert Systems.pdf - referencing inheritance chains in a taxonomy)
- Important Idea: Concepts like intermediaries and preclusion are introduced to handle potential conflicts or exceptions in inheritance hierarchies, especially in multiple inheritance scenarios where different paths might suggest conflicting information.
- Quote: "A class y ∈ K is called an intermediary to an inheritance chain y1 ≤ . . . ≤ yn ∈ ΩT... if one of the following conditions is satisfied..." (Principles of Expert Systems.pdf)
- Quote: "A chain y1 ≤ . . . ≤ yn[a = c1] ∈ ΩT... is said to preclude a chain y1 ≤ . . . ≤ ym[a = c2] ∈ ΩT... if yn is an intermediary to y1 ≤ . . . ≤ ym." (Principles of Expert Systems.pdf)
- Important Idea: Frames can incorporate attributes with defined types (domains), and type functions help determine the expected values for attribute sequences within a taxonomy. Subtyping is related to the relationship between these attribute sequence types.
- Quote: "For each yi ∈ K, we define a type function τi : A∗ → K as follows..." (Principles of Expert Systems.pdf)
- Quote: "We say that y1 is a subtype of y2, denoted by is y1 ≤ y2, if the following two properties hold..." (Principles of Expert Systems.pdf)

### Reasoning with Uncertainty:
Expert systems often need to handle uncertain information. Several models for representing and reasoning with uncertainty are presented.
- Key Fact: Probability theory provides a formal framework for reasoning about chance events, but its application in expert systems can be challenging due to the need for extensive probability assessments. Concepts like conditional probability and Bayes' theorem are fundamental.
- Quote: "THEOREM 5.4 (Bayes’ theorem) Let P be a probability function on a sample space Ω. Let hi ⊆ Ω... be mutually exclusive and collectively exhaustive hypotheses... Furthermore, let ej1 , . . . , ejk ⊆ Ω... be pieces of evidence such that they are conditionally independent given any hypothesis hi. Then, the following property holds: P (hi | ej1 ∩ · · · ∩ ejk ) = [Formula]" (Principles of Expert Systems.pdf)
- Important Idea: Simplified models like the subjective Bayesian method and the certainty factor model (used in systems like MYCIN) were developed to address the practical difficulties of using full probability theory. Certainty factors represent degrees of belief or disbelief.
- Key Fact: The Dempster-Shafer theory offers an alternative approach using basic probability assignments and belief functions, allowing for representation of ignorance and combination of evidence using Dempster's rule.
- Quote: "Let Θ be a frame of discernment, and let m be a basic probability assignment on Θ. Then, the belief function... corresponding to m is the function Bel : 2Θ → [0, 1] defined by Bel(x) = ∑ y⊆x m(y) for each x ⊆ Θ." (Principles of Expert Systems.pdf)
- Important Idea: Network models, such as belief networks (Bayesian networks), represent dependencies between variables graphically and use propagation algorithms to update beliefs when new evidence is introduced.
- Quote: "Knowledge representation in a belief network... Evidence propagation in a belief network..." (Principles of Expert Systems.pdf - section headings)

### Generalization and Learning:
The sources touch upon mechanisms for learning and generalization in symbolic AI systems.
- Important Idea: Least General Generalization (LGG) is a method in Inductive Logic Programming (ILP) for finding the most specific generalization of two logical clauses. This involves finding LGGs of terms and literals.
- Quote: "To define the LGG of two clauses, we start with the LGG of terms: * lgg(f(s1,. . .,sn), f(t1,. . .,tm)) = f(lgg(s1,t1),. . . ,lgg(sn,tn)). * lgg(f(s1,. . .,sn), g(t1,. . .,tm)) = V (a variable)..." (Inductive logic programming at 30.pdf)
- Important Idea: Generalization and specialization rules are fundamental operations in learning systems. Examples include dropping conditions, replacing constants with variables, and generalizing by internal disjunction.
- Quote: "G en er al iz at io n an d sp ec ia liz at io n ru le s: 3 D ro pp in g co nd it io n? Y es ... C on st an ts t o va ri ab le s? Y es..." (Machine Learning_ An Artificial Intelligence Approach ( PDFDrive ).pdf)
- Important Idea: Learning can involve searching through hypothesis spaces, like the "attribute-only space" defined by a structural generalization, using techniques such as beam search.
- Quote: "Once the structure-only candidate set C has been built, each candidate generalization in C must be filled out by finding values for its attribute descrip­tors. Each candidate generalization g in C is used to define an attribute-only space that is then searched using a beam search technique similar to that used to search the structure-only space." (Machine Learning_ An Artificial Intelligence Approach ( PDFDrive ).pdf)
- Important Idea: Systems like BACON are mentioned as examples of discovery systems that rediscover scientific laws by analyzing data and postulating properties (like density or the displacement law). This involves defining new terms based on observed data relationships.
- Quote: "The system defines the ratio term ic v/o, a conjectured property, which has the con­stant value 1.0 for all objects..." (Machine Learning_ An Artificial Intelligence Approach ( PDFDrive ).pdf - referring to BACON)
- Important Idea: Learning heuristics or production rules from examples, as seen in the LEX system learning symbolic integration operators or systems modeling student behavior in algebra, is another form of machine learning discussed.
- Quote: "Over 40 problem-solving operators are currently provided to LEX, some of which are shown in Figure 6-1. Each operator is interpreted as follows: If the general pattern on the left hand side of the operator is found within the problem state, then that pattern may be replaced by the pattern specified on the right hand side of the operator." (Machine Learning_ An Artificial Intelligence Approach ( PDFDrive ).pdf)
- Quote: "Table 16-1: Rules and mal-rules in student models." (Machine Learning_ An Artificial Intelligence Approach ( PDFDrive ).pdf)

### System Implementation and User Interaction:
The implementation of AI systems using languages like PROLOG and LISP is discussed, highlighting their suitability for symbolic manipulation and logic programming.
- Key Fact: PROLOG is based on logic programming and uses Horn clauses. It is well-suited for implementing inference engines based on SLD resolution.
- Quote: "Horn clauses are employed in the programming language PROLOG. We will return to this observation in Section 2.7.2." (Principles of Expert Systems.pdf)
- Quote: "B ← A1, . . . , An where B, A1, . . . , An, n ≥ 0, are atomic formulas. Instead of the (reverse) implication symbol, in PROLOG usually the symbol :- is used, and clauses are terminated by a dot." (Principles of Expert Systems.pdf)
- Key Fact: LISP is a powerful language for symbolic processing, often used for AI research due to its flexible data structures (lists) and ability to manipulate code as data.
- Quote: "Fundamental principles of LISP... The LISP expression... The form... Procedural abstraction in LISP... Variables and their scopes." (Principles of Expert Systems.pdf - section headings)
- Important Idea: Expert systems require user interfaces that can provide explanations (e.g., "how" and "why" facilities) to justify their reasoning.
- Quote: "User interface and explanation... A user interface in PROLOG... The how facility... The why-not facility..." (Principles of Expert Systems.pdf - section headings)
- Important Idea: Systems like NANOKLAUS demonstrate interactive knowledge acquisition, where the system learns new concepts and relationships by being told and asking clarifying questions, including handling units of measurement and conversions.
- Quote: "FEET - got it. Thanks. 5_ A meter' is a unit of length How is it related to FOOT? There are 3.3 jeel in a meter. Now I understand METER. 6_ A physical object has a length So PHYSICAL OBJECTS have LENGTHS." (Machine Learning_ An Artificial Intelligence Approach ( PDFDrive ).pdf)
- Quote: "Whenever an additional unit of a measure is declared, NANOKLAUS requests the factor for conversion to one of the previously declared units." (Machine Learning_ An Artificial Intelligence Approach ( PDFDrive ).pdf)