---
title: "Structured Output from Large Language Models"
description: "How to make generative models produce data structures, database queries, and program code that machines can reliably consume."
date: 2026-03-19
lastmod: 2026-03-19
weight: 10
---
Large language models are remarkably good at producing human-readable prose, but production software systems rarely consume prose. They consume JSON payloads, SQL queries, API responses, and typed data structures. The gap between what an LLM naturally produces and what a downstream system can parse is the central engineering challenge of structured output.
<!--more-->
This article explains how text generation works at the token level, why unconstrained generation breaks structure, how constrained decoding closes that gap, what still goes wrong in practice, and how the OpenAI and Ollama APIs expose structured output to application developers.


## 1. How Text Generation Works

### The Autoregressive Loop

Every modern LLM generates text the same way: one token at a time. The process is deceptively simple.

1. The user's prompt is tokenized---split into subword units from a fixed vocabulary of roughly 50,000 to 100,000 entries---and converted to embedding vectors.
2. The transformer processes these embeddings through its layers, producing a probability distribution (a vector of *logits*) over the entire vocabulary.
3. A sampling strategy selects one token from that distribution.
4. The selected token is appended to the sequence, and steps 2--3 repeat until the model emits a stop token or hits a length limit.

Mathematically, at each step *t*, the model computes:

$$P(y_t \mid y_1, y_2, \ldots, y_{t-1}, x)$$

where $x$ is the input prompt and $y_t$ is the next token. The full output is the product of these conditional probabilities. This factorization is what makes the process *autoregressive*: each token conditions on every token that came before it.

### Sampling Strategies

The logit vector does not directly become a token. A *decoding strategy* determines how the probability distribution is used to make a selection. The choice of strategy has a profound effect on output quality and determinism.

| Strategy | Mechanism | Typical Use |
|---|---|---|
| Greedy decoding | Always select the highest-probability token | Deterministic output, but prone to repetition |
| Temperature sampling | Scale logits by a temperature $T$ before softmax | $T < 1$ sharpens the distribution; $T > 1$ flattens it |
| Top-*k* sampling | Restrict the candidate set to the *k* highest-probability tokens | Reduces nonsense by eliminating the long tail |
| Top-*p* (nucleus) sampling | Restrict to the smallest set whose cumulative probability exceeds *p* | Adapts candidate-set size to the model's confidence |
| Min-*p* sampling | Filter tokens whose probability falls below $p \times p_{\max}$ | A more recent alternative that scales with confidence |

A concrete example clarifies the role of temperature. Suppose the raw logits for the next token are `[2.0, 1.5, 0.5, 0.3]`. At temperature $T = 0.5$, these become `[4.0, 3.0, 1.0, 0.6]`---the differences are amplified, making the top token overwhelmingly likely. At $T = 2.0$, they become `[1.0, 0.75, 0.25, 0.15]`---the distribution is nearly uniform, and any token might be chosen. For structured output, low temperatures (or greedy decoding) are almost always preferable: determinism and consistency matter more than creativity.

### Why Unconstrained Generation Fails for Structure

The fundamental problem is that standard sampling has no awareness of structural constraints. The model "knows" JSON patterns---it has seen millions of JSON documents during training---but knowledge is not guarantee.

When asked to produce JSON, an unconstrained model might:

- Emit invalid syntax: `{"name": "John"` with a missing closing brace.
- Use incorrect types: `{"age": "twenty-five"}` when the schema expects an integer.
- Wrap the output in conversational text: `Sure! Here's the JSON: {...}`.
- Hallucinate fields that do not exist in the schema.

Each of these failures is a natural consequence of the model's training objective, which optimizes for plausible next-token prediction across all genres of text, not for structural validity in any particular format.


## 2. Constrained Decoding

### The Core Idea

Constrained decoding modifies the autoregressive loop so that the model *cannot* produce structurally invalid output. The modification is simple in principle: at each step, before sampling, set the logits of all invalid tokens to $-\infty$. After softmax, their probabilities become zero. The model can only choose from tokens that keep the partial output on a valid path through the target grammar.

The process has five steps:

1. **Compute logits.** The model produces its usual probability distribution.
2. **Evaluate constraints.** A grammar checker determines which tokens are valid given the current partial output and the target schema.
3. **Mask invalid tokens.** Invalid token logits are set to $-\infty$.
4. **Renormalize.** The remaining probabilities are adjusted to sum to 1.
5. **Sample.** A token is selected from the valid set only.

### Grammar-Based Generation

For formats with well-defined grammars---JSON, SQL, Python, YAML---the constraint checker can be implemented as a finite state machine or a context-free grammar parser that tracks the current position in the grammar and reports which tokens would constitute a legal continuation.

The following simplified example illustrates the idea for JSON generation:

```python
import numpy as np

class JSONConstrainedSampler:
    def __init__(self, schema):
        self.schema = schema

    def get_valid_tokens(self, current_text):
        """Determine valid next tokens based on JSON grammar and schema."""
        if current_text.endswith('"'):
            if self._in_key_position(current_text):
                return {':'}

        if current_text.rstrip().endswith(':'):
            field_type = self._get_expected_type(current_text)
            if field_type == 'string':
                return {'"'}
            elif field_type == 'number':
                return {'0','1','2','3','4','5','6','7','8','9','-'}
            elif field_type == 'boolean':
                return {'t', 'f'}

        return valid_tokens

    def constrained_sample(self, logits, current_text, token_to_char):
        """Sample from logits with JSON constraints applied."""
        valid_chars = self.get_valid_tokens(current_text)
        valid_token_ids = {
            tid for tid, char in token_to_char.items()
            if char in valid_chars
        }

        masked_logits = logits.copy()
        for tid in range(len(logits)):
            if tid not in valid_token_ids:
                masked_logits[tid] = float('-inf')

        probs = self._softmax(masked_logits)
        return np.random.choice(len(probs), p=probs)
```

In production systems, the grammar checker is far more sophisticated---handling nested objects, arrays, escape sequences, and the interaction between subword tokenization and character-level grammar rules---but the principle remains the same: restrict the sample space at every step.

### Benefits and Limitations

Constrained decoding offers three clear benefits. First, it *guarantees* syntactic validity: the output always conforms to the grammar. Second, it eliminates an entire class of parsing errors downstream. Third, it removes the need for extraction heuristics that strip conversational preamble or fix trailing commas.

It also has real limitations. Grammar checking at every token adds computational overhead. Subword tokenization complicates the mapping between tokens and grammar symbols---a single token might span a brace and the first character of a key. Most importantly, constrained decoding guarantees *syntax*, not *semantics*. A query can be perfectly valid SQL and still return the wrong data.


## 3. Pitfalls and Common Failure Modes

Even with constrained decoding guaranteeing syntactic validity, structured output from LLMs fails in predictable ways. Understanding these failure modes is essential for building robust systems.

### Database Query Generation

Analysis of large-scale LLM-generated SQL reveals consistent error patterns.

**Schema misunderstanding** accounts for 35--40% of errors. The model assumes conventional naming that does not match the actual schema. Asked to "show revenue by product for last month," it might write:

```sql
-- Wrong: assumes revenue is a column on products
SELECT p.name, p.revenue
FROM products p
WHERE p.created_at > '2026-02-01';

-- Correct: revenue is computed from order_items
SELECT p.name, SUM(oi.price * oi.quantity) AS revenue
FROM products p
JOIN order_items oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id
WHERE o.created_at > '2026-02-01'
GROUP BY p.name;
```

The root cause is pattern matching against training data where "revenue" and "products" frequently co-occur. The fix is to provide the complete schema with explicit relationships and, ideally, a semantic layer that defines valid join paths.

**Incorrect join paths** account for 25--30% of errors. The model attempts a direct join between tables that have no foreign key relationship, skipping intermediate tables:

```sql
-- Wrong: no direct relationship between customers and products
SELECT c.name, p.product_name, SUM(p.price)
FROM customers c
JOIN products p ON c.id = p.customer_id
GROUP BY c.name, p.product_name;

-- Correct: traverse through orders and order_items
SELECT c.name, p.product_name, SUM(oi.price * oi.quantity)
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
GROUP BY c.name, p.product_name;
```

**Wrong aggregation logic** accounts for 15--20% of errors, typically manifesting as missing columns in `GROUP BY` clauses or confusion between `SUM` and `AVG`.

**Missing business logic filters** produce queries that are technically correct but return wrong results because they include test accounts, soft-deleted records, or other data that business rules should exclude:

```sql
-- Naive: includes everything
SELECT COUNT(*) FROM customers;

-- Production-correct: applies business rules
SELECT COUNT(*)
FROM customers
WHERE status = 'active'
  AND is_test_account = false
  AND deleted_at IS NULL;
```

### Code Generation

LLM-generated code exhibits its own characteristic failures. Security vulnerabilities are the most dangerous---string interpolation in SQL queries, unsanitized user input in shell commands, missing authentication checks:

```python
# Vulnerable: SQL injection
def get_user(username):
    query = f"SELECT * FROM users WHERE name = '{username}'"
    return db.execute(query)

# Secure: parameterized query
def get_user(username):
    query = "SELECT * FROM users WHERE name = ?"
    return db.execute(query, (username,))
```

Type inconsistencies are common: a function annotated to return a `list` might return a `dict`. Edge cases are frequently unhandled---division by zero, empty collections, null values. These errors are not caught by constrained decoding because the *syntax* is valid; only the *semantics* are wrong.

### JSON Schema Violations

Even when using JSON mode (as opposed to full structured output), models frequently include explanatory text as extra fields, use string representations of numbers, or omit required fields. Full structured output with schema enforcement eliminates most of these issues, but "JSON mode" alone---which guarantees only that the output is valid JSON, not that it matches a particular schema---leaves them wide open.


## 4. Post-Processing Strategies

When constrained decoding is unavailable or insufficient, post-processing provides a safety net.

### Extraction and Cleanup

The simplest strategy handles models that wrap valid JSON in conversational text. A regex extracts the JSON object, and a fixup function repairs common formatting errors:

```python
import json
import re

def extract_json_from_llm_response(response: str) -> dict:
    """Extract JSON from an LLM response that may contain extra text."""
    response = response.strip()
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        json_str = json_match.group()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            json_str = fix_common_json_errors(json_str)
            return json.loads(json_str)
    raise ValueError("No valid JSON found in response")

def fix_common_json_errors(json_str: str) -> str:
    """Repair trailing commas, single quotes, and inline comments."""
    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
    json_str = json_str.replace("'", '"')
    json_str = re.sub(r'//.*?\n', '', json_str)
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
    return json_str
```

This is brittle---it will fail on nested JSON or strings containing braces---but it handles the most common cases and is a reasonable fallback when structured output is not supported by the model.

### Schema Validation with Pydantic

Extraction produces a dictionary; validation ensures it matches the expected schema. Pydantic models serve double duty: they define the schema for the LLM and validate its output.

```python
from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional

class ProductReview(BaseModel):
    product_name: str
    rating: int
    sentiment: str
    summary: Optional[str] = None

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

    @field_validator('sentiment')
    @classmethod
    def validate_sentiment(cls, v):
        allowed = {'positive', 'negative', 'neutral'}
        if v.lower() not in allowed:
            raise ValueError(f'Sentiment must be one of {allowed}')
        return v.lower()
```

### SQL Validation

For generated SQL, validation goes beyond parsing. A schema-aware validator checks that referenced tables and columns exist, that join paths are valid, and that aggregation logic is consistent:

```python
import sqlparse

class SQLValidator:
    def __init__(self, schema_info):
        self.schema = schema_info

    def validate_query(self, sql: str) -> tuple[bool, list[str]]:
        errors = []
        try:
            parsed = sqlparse.parse(sql)[0]
        except Exception as e:
            return False, [f"Parse error: {str(e)}"]

        tables = self._extract_tables(parsed)
        for table in tables:
            if table not in self.schema['tables']:
                errors.append(f"Table '{table}' does not exist")

        columns = self._extract_columns(parsed)
        for table, column in columns:
            if table in self.schema['tables']:
                if column not in self.schema['tables'][table]['columns']:
                    errors.append(
                        f"Column '{column}' does not exist in '{table}'"
                    )

        joins = self._extract_joins(parsed)
        for join in joins:
            if not self._is_valid_join_path(
                join['from_table'], join['to_table']
            ):
                errors.append(
                    f"Invalid join: {join['from_table']} -> {join['to_table']}"
                )

        return len(errors) == 0, errors
```

### Retry with Error Feedback

When validation fails, the most effective recovery strategy is to feed the error message back to the model and ask it to try again. This creates a closed loop: generate, validate, report errors, regenerate.

```python
async def generate_with_retry(prompt, validator_fn, max_retries=3):
    for attempt in range(max_retries):
        response = await llm_client.generate(prompt)
        try:
            return validator_fn(response)
        except ValidationError as e:
            if attempt < max_retries - 1:
                prompt = f"""{prompt}

Previous attempt failed validation:
{e}

Please correct these errors and try again."""
            else:
                raise Exception(f"Failed after {max_retries} attempts: {e}")
```

In practice, most validation failures are corrected on the first retry. Three attempts is usually sufficient; if the model cannot produce valid output in three tries, the prompt or schema likely needs redesigning.


## 5. API Implementations

### OpenAI Structured Output

OpenAI's structured output API guarantees schema adherence through server-side constrained decoding. The key distinction from the older "JSON mode" is that structured output enforces a specific schema, not merely valid JSON.

The Python SDK integrates directly with Pydantic:

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]
    location: str

class CalendarEvents(BaseModel):
    events: list[CalendarEvent]

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Extract calendar events from text."},
        {"role": "user", "content": (
            "Team meeting on March 20 with Alice, Bob "
            "at Conference Room A"
        )}
    ],
    response_format=CalendarEvents,
)

events = completion.choices[0].message.parsed
print(events.events[0].name)  # "Team meeting"
```

The `response_format` parameter accepts a Pydantic model class directly. The API converts it to a JSON schema, applies constrained decoding during generation, and returns a parsed object. No extraction or post-processing is needed.

For deterministic output---important when structured results feed into automated pipelines---set `temperature=0`:

```python
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=messages,
    response_format=MySchema,
    temperature=0,
)
```

### Ollama Structured Output

Ollama added structured output support in December 2024, bringing constrained decoding to locally hosted open-source models. The API accepts a JSON schema (not a Pydantic class directly, but Pydantic's `.model_json_schema()` method bridges the gap):

```python
from ollama import chat
from pydantic import BaseModel

class Pet(BaseModel):
    name: str
    animal: str
    age: int
    color: str | None
    favorite_toy: str | None

class PetList(BaseModel):
    pets: list[Pet]

response = chat(
    model='llama3.2',
    messages=[{
        'role': 'user',
        'content': (
            'I have two cats: Luna is 3 years old and black, '
            'Loki is 5 and orange.'
        )
    }],
    format=PetList.model_json_schema(),
)

pets = PetList.model_validate_json(response.message.content)
for pet in pets.pets:
    print(f"- {pet.name}: {pet.age} year old {pet.color} {pet.animal}")
```

The pattern works across Ollama's supported models---Llama, Mistral, Gemma, Qwen, and others---and extends to multimodal use cases. A vision model can produce structured descriptions of images:

```python
from typing import Literal, Optional

class Object(BaseModel):
    name: str
    confidence: float
    attributes: str

class ImageDescription(BaseModel):
    summary: str
    objects: list[Object]
    scene: str
    colors: list[str]
    time_of_day: Literal['Morning', 'Afternoon', 'Evening', 'Night']
    setting: Literal['Indoor', 'Outdoor', 'Unknown']
    text_content: Optional[str] = None

response = chat(
    model='llava',
    messages=[{
        'role': 'user',
        'content': 'Describe this photo and detect objects.',
        'images': ['path/to/photo.jpg'],
    }],
    format=ImageDescription.model_json_schema(),
    options={'temperature': 0},
)

description = ImageDescription.model_validate_json(response.message.content)
```

### Comparing the Two APIs

| Aspect | OpenAI | Ollama |
|---|---|---|
| Models | GPT-4o, GPT-4o-mini | Llama, Mistral, Gemma, Qwen, etc. |
| Hosting | Cloud API | Local or self-hosted |
| Cost | Per-token pricing | Free (hardware costs only) |
| Latency | Network-dependent | Local; faster for small models |
| Privacy | Data sent to OpenAI | Data stays on your machine |
| Output quality | Generally higher | Varies by model |
| Schema interface | `response_format=PydanticModel` | `format=PydanticModel.model_json_schema()` |

The choice between them is driven by the application's constraints. OpenAI offers higher-quality output from larger models with zero infrastructure overhead. Ollama offers data privacy, no per-token cost, and independence from external services. Many production systems use both: Ollama for development and sensitive data, OpenAI for customer-facing features where quality is paramount.


## 6. Best Practices

### Choosing Between Constrained Decoding and Post-Processing

Use native structured output (constrained decoding) when the schema is well-defined, validation is critical, and the API supports it. Fall back to post-processing when the output format is flexible, the model does not support structured output, or custom business-logic validation is required. In most cases, the right answer is both: use constrained decoding for syntactic validity and post-processing for semantic validation.

### Schema Design

Three principles lead to better output:

**Be explicit with types.** Use `int` instead of `str` for ages, `datetime` instead of `str` for timestamps, `bool` instead of `Optional` without a default. Ambiguous types force the model to guess, and its guesses will not always match yours.

```python
# Clear types improve output quality
class User(BaseModel):
    age: int
    created_at: datetime
    is_active: bool

# Vague types invite errors
class User(BaseModel):
    age: str          # forces the model to output "25" as a string
    metadata: dict    # too open-ended
```

**Use enums for constrained values.** When a field has a fixed set of valid values, an enum prevents the model from inventing alternatives:

```python
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str
    priority: Priority
```

**Provide field descriptions.** Pydantic's `Field` descriptor adds context that the model uses to make better choices:

```python
from pydantic import Field

class Product(BaseModel):
    name: str = Field(description="Product name as it appears in catalog")
    price: float = Field(description="Price in USD", ge=0)
    category: str = Field(description="One of: Electronics, Clothing, Food")
```

### Prompting for Structure

Even with constrained decoding, prompt quality affects output quality. Three strategies consistently help.

First, include the schema in the system prompt. The model produces better output when it can see the full structure it needs to fill, not just the field currently being generated.

Second, provide examples. Few-shot prompting---showing one or two input-output pairs before the real query---dramatically reduces errors, especially for complex schemas.

Third, for SQL generation, provide the complete database schema with explicit relationships, primary and foreign keys, and business rules (such as "always filter on `deleted_at IS NULL`"). The model cannot infer relationships it has never seen.

### The Full Pipeline

A production-grade structured output system combines constrained generation, schema validation, business-logic validation, and retry into a single pipeline:

```python
class StructuredOutputPipeline:
    def __init__(self, model, schema, max_retries=3):
        self.model = model
        self.schema = schema
        self.max_retries = max_retries

    async def generate(self, prompt):
        for attempt in range(self.max_retries):
            try:
                response = await self._llm_generate(prompt)
                extracted = self._extract_structured_data(response)
                validated = self.schema(**extracted)
                self._validate_business_rules(validated)
                return validated
            except ValidationError as e:
                if attempt < self.max_retries - 1:
                    prompt = self._add_error_feedback(prompt, e)
                else:
                    self._log_failure(prompt, response, e)
                    raise

    def _validate_business_rules(self, data):
        if hasattr(data, 'sql'):
            forbidden = ['DROP', 'DELETE', 'TRUNCATE']
            if any(kw in data.sql.upper() for kw in forbidden):
                raise ValueError("Forbidden SQL operation detected")
```

Each layer catches a different class of error. Constrained decoding ensures syntactic validity. Schema validation catches type mismatches and missing fields. Business-logic validation catches semantically dangerous output. Retry with error feedback recovers from the errors that slip through.


## 7. Summary

Structured output from LLMs rests on understanding five ideas:

1. **Text generation is autoregressive.** The model produces one token at a time, sampling from a probability distribution. Sampling parameters---temperature, top-*k*, top-*p*---control the tradeoff between determinism and diversity.

2. **Constrained decoding guarantees structure.** By masking invalid tokens at each generation step, the model can only produce output that conforms to a target grammar. Modern APIs from OpenAI and Ollama expose this as a simple parameter.

3. **Common pitfalls are predictable.** Schema misunderstanding, incorrect join paths, wrong aggregation, missing business filters, security vulnerabilities, and type mismatches account for the vast majority of errors.

4. **Post-processing remains essential.** Constrained decoding handles syntax; it cannot enforce semantic correctness. Validation with Pydantic, schema-aware SQL checking, and business-rule enforcement fill the gap.

5. **The combination is greater than the parts.** Constrained generation, schema validation, business-logic checks, and retry with error feedback form a pipeline that achieves production-grade reliability from inherently probabilistic models.

The field is moving quickly. As constrained decoding becomes standard across model providers and open-source frameworks, the syntactic failure modes will largely disappear. The semantic failures---wrong joins, missing filters, hallucinated relationships---will remain the harder problem, and addressing them will require richer schema representations, better prompt engineering, and tighter integration between LLMs and the systems they generate output for.

---

### References

1. UsedataBrain, "LLM SQL Evaluation," https://www.usedatabrain.com/blog/llm-sql-evaluation
2. Ollama Blog, "Structured Outputs," https://ollama.com/blog/structured-outputs
3. Ollama Documentation, "Structured Outputs," https://docs.ollama.com/capabilities/structured-outputs
4. OpenAI Developer Documentation, "Structured Outputs," https://developers.openai.com/api/docs/guides/structured-outputs/
5. OpenAI Blog, "Introducing Structured Outputs in the API," https://openai.com/index/introducing-structured-outputs-in-the-api/
6. Brenddoerfer, M., "Constrained Decoding: Structured LLM Output," https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output
7. Aman.ai, "Token Sampling," https://aman.ai/primers/ai/token-sampling/
8. Thoughtworks, "Min-p Sampling for LLMs," https://www.thoughtworks.com/en-us/insights/blog/generative-ai/Min-p-sampling-for-LLMs
9. AWS Machine Learning Blog, "Enterprise-grade Natural Language to SQL Generation Using LLMs," https://aws.amazon.com/blogs/machine-learning/enterprise-grade-natural-language-to-sql-generation-using-llms-balancing-accuracy-latency-and-scale/

