---
draft: false
title: Pizza Ontology
weight: 31
description: Example of an ontology to descrinbe pizza
date: 2024-01-01
lastmod: 2024-01-01
---

# Pizza Ontology in OWL

## The Full OWL/Turtle Serialization

Below is the complete pizza ontology in **Turtle syntax** (a readable OWL serialization), with every construct labeled:

```turtle
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix pizza: <http://example.org/pizza#> .

# ─────────────────────────────────────────────
#  ONTOLOGY DECLARATION
# ─────────────────────────────────────────────
<http://example.org/pizza> a owl:Ontology .

# ─────────────────────────────────────────────
#  TBOX — Terminological Knowledge (Classes & Properties)
# ─────────────────────────────────────────────

# Top-level classes
pizza:Pizza          a owl:Class .
pizza:PizzaBase      a owl:Class .
pizza:PizzaTopping   a owl:Class .

# Topping subclasses (disjoint!)
pizza:CheeseTopping  a owl:Class ; rdfs:subClassOf pizza:PizzaTopping .
pizza:VegTopping     a owl:Class ; rdfs:subClassOf pizza:PizzaTopping .
pizza:MeatTopping    a owl:Class ; rdfs:subClassOf pizza:PizzaTopping .

# More specific toppings
pizza:MozzarellaTopping a owl:Class ; rdfs:subClassOf pizza:CheeseTopping .
pizza:TomatoTopping     a owl:Class ; rdfs:subClassOf pizza:VegTopping .
pizza:PepperoniTopping  a owl:Class ; rdfs:subClassOf pizza:MeatTopping .
pizza:MushroomTopping   a owl:Class ; rdfs:subClassOf pizza:VegTopping .

# Base subclasses
pizza:ThinBase         a owl:Class ; rdfs:subClassOf pizza:PizzaBase .
pizza:ThickBase        a owl:Class ; rdfs:subClassOf pizza:PizzaBase .

# Disjointness — ensures a MeatTopping cannot also be a VegTopping
[] a owl:AllDisjointClasses ;
   owl:members ( pizza:CheeseTopping pizza:VegTopping pizza:MeatTopping ) .

[] a owl:AllDisjointClasses ;
   owl:members ( pizza:ThinBase pizza:ThickBase ) .

# ── Object Properties ──
pizza:hasTopping a owl:ObjectProperty ;
    rdfs:domain pizza:Pizza ;
    rdfs:range  pizza:PizzaTopping .

pizza:hasBase a owl:ObjectProperty ;
    rdfs:domain pizza:Pizza ;
    rdfs:range  pizza:PizzaBase ;
    a owl:FunctionalProperty .         # Each pizza has exactly one base

# ── Named Pizza Types (defined classes) ──
pizza:MargheritaPizza a owl:Class ;
    rdfs:subClassOf pizza:Pizza ;
    rdfs:subClassOf
        [ a owl:Restriction ;
          owl:onProperty pizza:hasTopping ;
          owl:someValuesFrom pizza:TomatoTopping ] ;
    rdfs:subClassOf
        [ a owl:Restriction ;
          owl:onProperty pizza:hasTopping ;
          owl:someValuesFrom pizza:MozzarellaTopping ] .

pizza:VegetarianPizza a owl:Class ;
    owl:equivalentClass
        [ a owl:Class ;
          owl:intersectionOf (
              pizza:Pizza
              [ a owl:Restriction ;
                owl:onProperty pizza:hasTopping ;
                owl:allValuesFrom
                    [ owl:unionOf ( pizza:CheeseTopping pizza:VegTopping ) ] ]
          ) ] .

pizza:PepperoniPizza a owl:Class ;
    rdfs:subClassOf pizza:Pizza ;
    rdfs:subClassOf
        [ a owl:Restriction ;
          owl:onProperty pizza:hasTopping ;
          owl:someValuesFrom pizza:PepperoniTopping ] .

# ─────────────────────────────────────────────
#  ABOX — Assertional Knowledge (Individuals)
# ─────────────────────────────────────────────

pizza:myMargherita a pizza:MargheritaPizza ;
    pizza:hasBase    pizza:myThinBase ;
    pizza:hasTopping pizza:myMozzarella, pizza:myTomato .

pizza:myThinBase   a pizza:ThinBase .
pizza:myMozzarella a pizza:MozzarellaTopping .
pizza:myTomato     a pizza:TomatoTopping .

pizza:studentPizza a pizza:Pizza ;
    pizza:hasBase    pizza:myThickBase ;
    pizza:hasTopping pizza:myMozzarella, pizza:myMushroom .

pizza:myThickBase  a pizza:ThickBase .
pizza:myMushroom   a pizza:MushroomTopping .
```


***

## OWL Expression Glossary

Here is what each major construct means:[^1][^2]


| Expression | Meaning |
| :-- | :-- |
| `a owl:Class` | Declares a named class |
| `rdfs:subClassOf` | Subsumption: every member of A is also in B |
| `owl:equivalentClass` | Two class expressions have the same extension |
| `owl:AllDisjointClasses` | No individual can belong to more than one listed class |
| `owl:ObjectProperty` | A binary relation between individuals |
| `owl:FunctionalProperty` | Each subject has **at most one** value for this property |
| `rdfs:domain / rdfs:range` | Type constraints on a property's subject/object |
| `owl:Restriction` | Anonymous class defined by a property constraint |
| `owl:someValuesFrom` | Existential restriction — ∃ *p* . *C* (at least one filler of type C) |
| `owl:allValuesFrom` | Universal restriction — ∀ *p* . *C* (all fillers must be type C) |
| `owl:intersectionOf` | Class intersection (logical AND) |
| `owl:unionOf` | Class union (logical OR) |


***

## TBox vs ABox

These two components together form the **Knowledge Base** in Description Logic:[^3][^4]

- **TBox (Terminological Box)** — the *schema*. It contains class declarations, subclass axioms, property definitions, restrictions, and equivalences. Everything above the ABox section in the Turtle above is TBox. Think of it as "what kinds of things exist and how are they related."
- **ABox (Assertional Box)** — the *data*. It contains named individuals (`pizza:myMargherita`, `pizza:myMozzarella`) and assertions about them (their types and property values). It answers "what specific things exist."

A key insight: **reasoning bridges the two**. The ABox says `pizza:studentPizza hasTopping myMozzarella, myMushroom`. The TBox says `VegetarianPizza ≡ Pizza ∧ ∀hasTopping.(CheeseTopping ⊔ VegTopping)`. A reasoner can then *infer* that `studentPizza` is a `VegetarianPizza` — even though you never stated it explicitly.[^1]

***

## Common Reasoning Tasks

OWL reasoners (HermiT, Pellet, Openllet) perform several standard tasks:[^5][^2]

### 1. Subsumption / Class Hierarchy

*"Is MargheritaPizza a subtype of Pizza?"*
The reasoner checks whether every model satisfying `MargheritaPizza` also satisfies `Pizza`. This is used to auto-classify the hierarchy.

### 2. Instance Classification (ABox Reasoning)

*"What type is `studentPizza`?"*
Given its toppings are `MozzarellaTopping` (a `CheeseTopping`) and `MushroomTopping` (a `VegTopping`), the `allValuesFrom` restriction on `VegetarianPizza` is satisfied → **`studentPizza` is inferred to be a `VegetarianPizza`**.

### 3. Consistency Checking

*"Can a pizza have a PepperoniTopping AND be a VegetarianPizza?"*
Since `MeatTopping` and `VegTopping` are disjoint, and `PepperoniTopping ⊑ MeatTopping`, the `allValuesFrom` restriction on `VegetarianPizza` would be violated → the ontology becomes **inconsistent** for such an individual.

### 4. Realization

*"What is the most specific type of `myMargherita`?"*
The reasoner finds the most specific named class that `myMargherita` belongs to: `MargheritaPizza`.

***

## SPARQL Queries on the Pizza Ontology

These queries run against an Apache Jena Fuseki or similar SPARQL endpoint loaded with the ontology above.[^6][^1]

**Q1 — Find all pizzas and their toppings:**

```sparql
PREFIX pizza: <http://example.org/pizza#>

SELECT ?pizza ?topping WHERE {
  ?pizza a pizza:Pizza .
  ?pizza pizza:hasTopping ?topping .
}
```

**Q2 — Find all subclasses of PizzaTopping:**

```sparql
PREFIX pizza: <http://example.org/pizza#>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?toppingType WHERE {
  ?toppingType rdfs:subClassOf+ pizza:PizzaTopping .
}
```

The `+` operator follows the subclass chain transitively, so this returns `CheeseTopping`, `VegTopping`, `MozzarellaTopping`, `TomatoTopping`, etc.[^1]

**Q3 — Find all pizzas that have a TomatoTopping (schema-level):**

```sparql
PREFIX pizza: <http://example.org/pizza#>
PREFIX owl:   <http://www.w3.org/2002/07/owl#>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?pizzaClass WHERE {
  ?pizzaClass rdfs:subClassOf+ pizza:Pizza .
  ?pizzaClass rdfs:subClassOf [
      a owl:Restriction ;
      owl:onProperty pizza:hasTopping ;
      owl:someValuesFrom pizza:TomatoTopping
  ] .
}
```

This returns `MargheritaPizza` at the TBox level.[^1]

**Q4 — Inferred vegetarian pizzas (requires reasoner active):**

```sparql
PREFIX pizza: <http://example.org/pizza#>

SELECT ?p WHERE {
  ?p a pizza:VegetarianPizza .
}
```

Without a reasoner, this returns nothing (no pizza was *asserted* as `VegetarianPizza`). **With HermiT/Pellet running**, it infers and returns `pizza:studentPizza` automatically — this is the power of OWL reasoning.[^5]

***

## Inductive Logic Programming (ILP) with the Pizza Ontology

ILP learns general rules from specific examples and background knowledge. Given the pizza ontology as background, the goal is to **induce** rules like "what makes a pizza vegetarian?"[^7]

### Background Knowledge (Prolog/Datalog facts from the ABox)

```prolog
% ABox as Prolog facts
hasTopping(myMargherita, myMozzarella).
hasTopping(myMargherita, myTomato).
hasTopping(studentPizza, myMozzarella).
hasTopping(studentPizza, myMushroom).

% TBox encoded as type hierarchy
mozzarellaTopping(myMozzarella).
tomatoTopping(myTomato).
mushroomTopping(myMushroom).

cheeseTopping(X) :- mozzarellaTopping(X).
vegTopping(X)    :- tomatoTopping(X).
vegTopping(X)    :- mushroomTopping(X).
```


### Positive and Negative Examples

```prolog
% Positive: these ARE vegetarian
pos(vegetarianPizza(myMargherita)).
pos(vegetarianPizza(studentPizza)).

% Negative: these are NOT vegetarian (a pepperoni pizza)
neg(vegetarianPizza(myPepperoni)).
```


### ILP Learning Task

An ILP system (e.g., **FOIL**, **Aleph**, or **Popper**) is given $B, E^+, E^-$ and must find hypothesis $H$ such that $B \cup H \models E^+$ and $B \cup H \not\models E^-$.[^7]

**Induced Rule (what the ILP system learns):**

```prolog
vegetarianPizza(P) :-
    pizza(P),
    hasTopping(P, T),
    \+ meatTopping(T).
```

This reads: *"A pizza is vegetarian if it is a pizza and none of its toppings are meat toppings."* The system **generalized** this rule from the examples — it was never told the definition, only given instances.[^8][^7]

### Why This Connects to the Ontology

The TBox's `owl:equivalentClass` definition of `VegetarianPizza` using `allValuesFrom` is essentially the same semantics as the induced Prolog rule — ILP **re-discovers ontological definitions** from data. This makes ILP a powerful complement to ontology learning: you can use ILP to mine rules from ABox data and promote them to TBox axioms.[^9][^7]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16]</span>

<div align="center">⁂</div>

[^1]: https://csiro-enviro-informatics.github.io/info-engineering/tutorials/tutorial-intro-to-rdf-and-owl.html

[^2]: https://cs.uwaterloo.ca/~a78khan/docs/PizzaOntologyReview.pdf

[^3]: https://www.michaeldebellis.com/post/using-sparql-subgraphs-to-segment-tbox-and-abox

[^4]: https://stackoverflow.com/questions/36276986/get-tbox-axioms-with-owl-api

[^5]: https://www.uio.no/studier/emner/matnat/ifi/IN3060/v20/exercises/owl_solutions.pdf

[^6]: https://stackoverflow.com/questions/45153600/sparql-query-on-pizza-ontology

[^7]: https://en.wikipedia.org/wiki/Inductive_logic_programming

[^8]: https://swi-prolog.discourse.group/t/popper-inductive-logic-programming-ilp-and-my-popper-page/3929

[^9]: https://www.cs.nmsu.edu/~ipivkina/Spring05cs579/StudentPres/inductiveLP.pdf

[^10]: https://protege.stanford.edu/conference/2009/tutorials.html

[^11]: https://people.cs.vt.edu/~kafura/ComputationalThinking/Class-Notes/Tutorial-Highlighted-Day1.pdf

[^12]: https://www.youtube.com/watch?v=kK5iLNNqZnc

[^13]: https://aispace.org/exercises/exercise13-a-1.shtml

[^14]: https://www.youtube.com/watch?v=VFbVYioceLI

[^15]: https://www.youtube.com/watch?v=TKMW5udKzIM

[^16]: https://owlready2.readthedocs.io/en/latest/sparql.html

