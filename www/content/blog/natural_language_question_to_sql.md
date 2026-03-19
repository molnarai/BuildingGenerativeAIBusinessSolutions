---
title: "Generating SQL from Natural Language with Ollama"
description: "Natural language to SQL (text-to-SQL) is one of the most practical applications of local LLMs."
date: 2026-03-19
lastmod: 2026-03-19
weight: 11
---
Natural language to SQL (text-to-SQL) is one of the most practical applications of local LLMs. This article walks through building a robust, production-quality pipeline using Ollama — from prompt construction to structured output validation and self-correction.


Running SQL generation locally via Ollama gives you full control over data privacy (no query or schema leaves your infrastructure), dialect customization, and the ability to fine-tune prompts without API rate limits. For research and educational systems handling sensitive data, this is often a hard requirement.



## Choosing the Right Model

Not all models are equally suited for SQL generation. Look for these attributes when selecting a model:

- **SQL-specific fine-tuning** — models trained on text-to-SQL benchmark datasets like Spider or WikiSQL significantly outperform general-purpose models
- **Instruction-following quality** — the model must reliably respect schema constraints and structured output format
- **Context window** — large schemas consume tokens quickly; aim for at least 8K context
- **Quantization level** — prefer Q6 or Q8 quantization for SQL tasks where precision matters over raw speed
- **Parameter count vs. hardware** — more parameters improve reasoning quality but must fit in available VRAM
- **Support structured output** - models that support [structured output](../structured_llm_output/) will be less likely to add non-ASCII characters into the query code

The following models are well-suited for text-to-SQL on Ollama:

| Model | Pull Command | Notes |
|---|---|---|
| **SQLCoder** | `ollama pull sqlcoder` | Purpose-built for text-to-SQL; fine-tuned on StarCoder; best starting point |
| **Qwen2.5-Coder 14B** | `ollama pull qwen2.5-coder:14b` | Strong instruction following, fast, excellent for structured output |
| **DeepSeek-Coder V2** | `ollama pull deepseek-coder-v2` | Broad code generation including complex SQL |
| **IBM Granite 20B** | `ollama pull granite-code:20b` | Evaluated specifically for enterprise SQL generation |
| **LLaMA 3 70B** | `ollama pull llama3:70b` | Best general reasoning for complex multi-table business logic |

**Practical recommendation:** Start with `sqlcoder` for pure SQL tasks. Use `qwen2.5-coder:14b` when you need a balance of speed and accuracy in an agentic retry loop. Fall back to `llama3:70b` for queries involving complex business logic or ambiguous natural language.



## Structured Output: The `format` Parameter

Ollama's `format` parameter is the key mechanism for ensuring the model returns parseable, executable SQL. There are two levels:

- **`"format": "json"`** — tells the model to return valid JSON, but with no constraints on structure. The model might return SQL mixed with commentary, missing fields, or inconsistent keys.
- **`"format": { JSON Schema }`** — compiles a GBNF grammar specific to your schema and constrains token generation at the engine level. The output *must* conform to your schema or generation fails.

For SQL generation, always use the second option with an explicit schema.

### Why Ask for Both `sql` and `explanation`?

Defining two separate fields — `sql` and `explanation` — is a deliberate design choice that improves output quality significantly:

1. **Chain-of-thought effect:** When forced to produce an `explanation`, the model reasons about the query intent before committing to SQL. This mirrors the "think before you answer" prompting pattern and tends to produce more accurate queries.
2. **Clean SQL field:** Without a separate explanation field, models often mix commentary into the SQL string (e.g., `"Here's a query that finds... SELECT * FROM..."`), which breaks direct execution. The schema enforces a clean split.
3. **Debuggability:** When a query is wrong, the explanation tells you *what the model thought you were asking*. If you asked for "top customers by revenue" and the explanation says "sorted by order count," the problem is in your prompt — not the SQL.
4. **Schema as a forcing function:** Requiring two non-optional fields means the GBNF grammar engine rejects incomplete responses, raising the bar for output completeness.

```python
from pydantic import BaseModel

class SQLQuery(BaseModel):
    sql: str
    explanation: str
```

Pass this to Ollama as:

```python
format=SQLQuery.model_json_schema()
```



## Structuring the Prompt

Prompt structure is the single largest lever for SQL generation quality. A well-structured prompt has four distinct sections: system instructions, schema context, few-shot examples, and the user question.

### Section 1: System Prompt

Define the model's role, the SQL dialect, and hard behavioral constraints:

```
You are an expert PostgreSQL query generator.
- Generate only SELECT statements. Never use INSERT, UPDATE, DELETE, or DROP.
- Use only the tables and columns defined in the schema below.
- Always use table aliases for clarity in multi-table queries.
- Do not include markdown formatting or explanation in the sql field.
```

Setting the dialect explicitly (PostgreSQL, MySQL, SQLite) prevents the model from using incompatible syntax — for example, using `LIMIT` in SQL Server or `TOP` in PostgreSQL.

### Section 2: Schema Context

This is the most critical section and the source of most SQL generation failures. Provide the schema in DDL format — `CREATE TABLE` statements — because this mirrors what models saw during training and encodes relationships unambiguously:

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name        VARCHAR(100),
    email       VARCHAR(100),
    region      VARCHAR(50),
    created_at  TIMESTAMP
);

CREATE TABLE orders (
    order_id    SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    amount      NUMERIC(10,2),
    status      VARCHAR(20),  -- values: 'pending', 'shipped', 'delivered'
    order_date  DATE
);
```

Key practices:
- Add **inline comments** on columns with constrained values — this prevents the model from hallucinating enum values like `WHERE status = 'complete'` instead of `'delivered'`
- Include **foreign key relationships** explicitly — they are essential for correct JOIN generation
- For large databases with many tables, **only include tables relevant to the query** — full schema dumps waste context and increase hallucination risk

### Section 3: Few-Shot Examples

Two or three natural language → SQL pairs dramatically anchor the output pattern, especially for dialect-specific syntax and date arithmetic:

```sql
-- Example 1
-- Question: How many orders were placed last month?
-- SQL: SELECT COUNT(*) FROM orders
--      WHERE order_date >= date_trunc('month', now() - interval '1 month')
--      AND order_date < date_trunc('month', now());

-- Example 2
-- Question: Top 5 customers by total spend
-- SQL: SELECT c.name, SUM(o.amount) AS total_spend
--      FROM customers c
--      JOIN orders o ON c.customer_id = o.customer_id
--      GROUP BY c.customer_id
--      ORDER BY total_spend DESC
--      LIMIT 5;
```

Choose examples that cover patterns likely to appear in your domain — aggregations, date ranges, and JOINs are the most common failure points.

### Section 4: The User Question

Place the actual question last, clearly delimited, with a SQL continuation primer:

```
-- Question: {user_question}
-- SQL:
```

The trailing `-- SQL:` is a prompting trick that primes the model to continue with a query rather than an explanation, since it resembles the format it was trained on.

### Full Assembled Template

```python
from ollama import chat

SYSTEM_PROMPT = """You are an expert PostgreSQL query generator.
Only generate SELECT statements using the schema provided.
Never reference tables or columns not in the schema.
Use table aliases in all multi-table queries."""

SCHEMA_DDL = """
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name        VARCHAR(100),
    email       VARCHAR(100),
    region      VARCHAR(50),
    created_at  TIMESTAMP
);
CREATE TABLE orders (
    order_id    SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    amount      NUMERIC(10,2),
    status      VARCHAR(20),  -- values: 'pending', 'shipped', 'delivered'
    order_date  DATE
);
"""

FEW_SHOT_EXAMPLES = """
-- Question: How many orders were placed last month?
-- SQL: SELECT COUNT(*) FROM orders WHERE order_date >= date_trunc('month', now() - interval '1 month') AND order_date < date_trunc('month', now());

-- Question: Top 5 customers by total spend
-- SQL: SELECT c.name, SUM(o.amount) AS total_spend FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id ORDER BY total_spend DESC LIMIT 5;
"""

def build_messages(user_question: str) -> list:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Schema:
{SCHEMA_DDL}

Examples:
{FEW_SHOT_EXAMPLES}

-- Question: {user_question}
-- SQL:
"""}
    ]
```



## Validation: Two Layers

Ollama's structured output guarantees a valid JSON object with a `sql` string field — nothing more. A response like `"sql": "SELEKT * FORM users"` fully satisfies the schema. Validation is therefore a separate, mandatory step.

### Layer 1: Syntax Validation with sqlglot

`sqlglot` parses SQL and returns structured, dialect-aware errors:

```python
import sqlglot

def validate_sql(sql: str, dialect: str = "postgres") -> tuple[bool, str]:
    try:
        sqlglot.parse_one(sql, dialect=dialect)
        return True, ""
    except sqlglot.errors.ParseError as e:
        return False, str(e)
```

### Layer 2: Run and Catch Database Errors

For read-only SELECT pipelines, executing the query and catching the database error is often the *better* feedback signal than static schema validation. PostgreSQL in particular returns highly informative messages:

```
ERROR: column "custmer_id" does not exist
LINE 1: SELECT custmer_id FROM orders
HINT: Did you mean "customer_id"?
```

This message — verbatim — can be fed back to Ollama for self-correction.

**Always enforce read-only access at the database level** by connecting with a role that has only SELECT privileges, regardless of what the prompt instructs:

```sql
CREATE ROLE query_agent LOGIN PASSWORD 'secret';
GRANT CONNECT ON DATABASE mydb TO query_agent;
GRANT USAGE ON SCHEMA public TO query_agent;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO query_agent;
```



## The Self-Correction Loop

Combining structured output, syntax validation, and live database error feedback into a retry loop produces a robust, self-healing pipeline:

```python
import sqlglot
import psycopg2
from ollama import chat
from pydantic import BaseModel

class SQLQuery(BaseModel):
    sql: str
    explanation: str

def generate_sql(user_question: str, max_retries: int = 3) -> SQLQuery:
    messages = build_messages(user_question)
    
    for attempt in range(max_retries):
        response = chat(
            model="sqlcoder",
            messages=messages,
            format=SQLQuery.model_json_schema(),
            options={"temperature": 0}
        )
        result = SQLQuery.model_validate_json(response.message.content)
        
        # Layer 1: syntax check
        valid, syntax_error = validate_sql(result.sql)
        if not valid:
            messages.append({"role": "assistant", "content": response.message.content})
            messages.append({"role": "user", "content": f"The SQL has a syntax error: {syntax_error}. Please fix it."})
            continue
        
        # Layer 2: execute against read-only connection
        try:
            conn = psycopg2.connect(dsn="postgresql://query_agent:secret@localhost/mydb")
            cur = conn.cursor()
            cur.execute(result.sql)
            rows = cur.fetchall()
            return result, rows
        except psycopg2.Error as e:
            messages.append({"role": "assistant", "content": response.message.content})
            messages.append({"role": "user", "content": f"The query failed with: {e}. Please fix it."})
    
    raise RuntimeError(f"Failed to generate valid SQL after {max_retries} attempts")
```

Setting `temperature: 0` ensures deterministic generation on the first attempt and meaningful variation on retries when the conversation history changes.



## Schema Retrieval for Large Databases

If your database has dozens of tables, don't dump the full schema into the prompt — that wastes context and introduces noise that increases hallucination risk. Instead, embed your table and column descriptions into a vector store and retrieve only the top-k most relevant tables per query. This integrates naturally with a RAG pipeline:

1. **Embed** each table's DDL + description at startup
2. **Retrieve** top-3 to top-5 relevant tables using the user question as the query
3. **Inject** only those DDL blocks into the prompt's schema section

This keeps prompts lean, improves accuracy, and scales to enterprise-sized schemas without hitting context limits.

## References
- [SQLGlot](https://github.com/tobymao/sqlglot) is a no-dependency SQL parser, transpiler, optimizer, and engine. It can be used to format SQL or translate between 31 different dialects like DuckDB, Presto / Trino, Spark / Databricks, Snowflake, and BigQuery. It aims to read a wide variety of SQL inputs and output syntactically and semantically correct SQL in the targeted dialects.
- [Pydantic](https://github.com/pydantic/pydantic) is a popular Python library for data validation, serialization, and settings management that leverages Python type hints. It ensures that data structures—such as API inputs or configuration—conform to defined types and constraints, enforcing "fail-fast" validation at runtime rather than when the data is later used.
- The article "[Structured Output from Large Language Models](../structured_llm_output/)" explains how text generation works at the token level, why unconstrained generation breaks structure, how constrained decoding closes that gap, what still goes wrong in practice, and how the OpenAI and Ollama APIs expose structured output to application developers.