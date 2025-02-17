+++
date = '2025-01-06T18:20:46-05:00'
due_date = "2025-04-07"
draft = false
title = 'Homework 4: Extracting Financial Information from SEC 10-K Filing'
weight = 40
status = '*not ready to start*'
+++

You will build a process to extract structured financial information and key terms from SEC 10-K filings. The goal is to transform unstructured text in HTML files into a structured data table. This assignment will help you experience the end-to-end process of preprocessing, extracting, and validating data from large text documents.
<!-- mode -->
---

### Instructions

#### 1. Preprocessing the HTML Files
You will begin by cleaning and preparing the HTML files for processing.

- **Steps**:
  1. Use `BeautifulSoup` to parse the HTML content.
  2. Remove unnecessary elements like `<script>` and `<style>` tags.
  3. Extract plain text from the HTML.
  4. Split the text into manageable chunks (e.g., 2000 words per chunk).
  5. Identify relevant sections (e.g., "Financial Statements," "Management Discussion and Analysis (MD&A)," "Risk Factors") using keyword-based patterns.

<!-- - **Code Example**:
   ```python
   from bs4 import BeautifulSoup
   import re

   def preprocess_html(content):
       soup = BeautifulSoup(content, 'html.parser')
       for script_or_style in soup(['script', 'style']):
           script_or_style.decompose()
       text = soup.get_text(separator=' ')
       text = re.sub(r'\s+', ' ', text).strip()
       return text

   def chunk_text(text, max_length=2000):
       words = text.split()
       return [' '.join(words[i:i + max_length]) for i in range(0, len(words), max_length)]

   def identify_relevant_sections(text):
       patterns = {
           'financial_statements': r'(?i)(financial statements|consolidated balance sheets|income statement)',
           'md&a': r'(?i)(management discussion and analysis|MD&A)',
           'risk_factors': r'(?i)(risk factors)'
       }
       sections = {section: re.search(pattern, text) for section, pattern in patterns.items()}
       return {k: v.group() if v else None for k, v in sections.items()}
   ``` -->

---

#### 2. Prompt Engineering for Data Extraction
After preprocessing, use a language model to extract specific financial data and key terms from identified sections.

- **Steps**:
  1. Design prompts tailored to extract specific information (e.g., "Extract revenue and net income").
  2. Apply these prompts to each chunk of text within the relevant sections.
  3. Format the extracted information as structured data (e.g., JSON).

<!-- - **Code Example**:
   ```python
   def extract_financial_data(chunk, section):
       # Simulated prompt engineering
       if section == 'financial_statements':
           if 'Revenue' in chunk:
               return {"Revenue": "$1,000,000"}
           elif 'Net Income' in chunk:
               return {"Net Income": "$500,000"}
       elif section == 'md&a':
           if 'performance' in chunk:
               return {"Performance": "Company performance improved."}
       elif section == 'risk_factors':
           if 'risks' in chunk:
               return {"Risks": "Market risks include..."}
       return {}
   ``` -->

---

#### 3. Post-Processing and Data Table Creation
You will transform the extracted information into a structured format like a Pandas DataFrame.

- **Steps**:
  1. Combine extracted data into rows where each row corresponds to a file and section.
  2. Create a table with columns such as `File Name`, `Section`, `Revenue`, `Net Income`, etc.

<!-- - **Code Example**:
   ```python
   import pandas as pd

   def create_data_table(extracted_data):
       rows = []
       for file_name, sections in extracted_data.items():
           for section, data in sections.items():
               row = {"File Name": file_name, "Section": section}
               row.update(data)
               rows.append(row)
       return pd.DataFrame(rows)
   ``` -->

---

#### 4. Validation
Validate the extracted data to ensure accuracy and completeness.

- **Steps**:
  1. Check for missing values or inconsistencies.
  2. Generate a validation report summarizing issues.
  
<!-- - **Code Example**:
   ```python
   def validate_data(data_table):
       missing_values = data_table.isnull().sum()
       validation_report = {
           "missing_values": missing_values.to_dict(),
           "is_valid": missing_values.sum() == 0
       }
       return validation_report
   ``` -->

---

#### 5. Execution on Batch Files
Once your program is complete, execute it on a batch of SEC filings provided by the department's server.

- The batch directory will contain multiple HTML files representing different SEC filings.
- Your program should loop through all files, preprocess them, extract relevant information, and output a consolidated data table.

---

### Deliverables
1. **Python Script**: Submit your complete Python script with all preprocessing, extraction, post-processing, and validation steps.
2. **Data Table**: Provide the final structured data table as a CSV file.
3. **Validation Report**: Include a summary of your validation results (e.g., missing values or inconsistencies).
4. **Documentation**: Write brief documentation explaining your approach and any challenges faced.

---

### Evaluation Criteria
Your submission will be graded based on:
1. **Correctness (40%)**: Does your program correctly extract financial information?
2. **Completeness (20%)**: Are all required fields (e.g., revenue, net income) extracted and included in the final table?
3. **Efficiency (20%)**: Is your code efficient and able to handle multiple files?
4. **Validation (10%)**: Did you validate your results effectively?
5. **Documentation (10%)**: Is your approach clearly explained?

---

<!-- ### Notes:
- Pre-downloaded SEC filings are available in the directory `/data/sec_filings/`.
- Use simulated responses or OpenAI/other LLM APIs for prompt engineering if needed.
- Ensure your code handles edge cases like missing sections or incomplete data gracefully.
 -->
