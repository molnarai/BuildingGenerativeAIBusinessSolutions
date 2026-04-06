---
date: 2026-03-09
classdates: 'Monday 2026-03-09, Wednesday 2026-03-04'
draft: false
title: 'NLP & Text Processing'
weight: 80
numsession: 8
---
This session explores how traditional NLP techniques function as a vital foundation for modern agentic AI systems rather than being replaced by them.
<!--more-->

It outlines a hybrid approach where deterministic tools like regular expressions, HTML parsers, and grammatical rules handle the initial cleaning and structuring of messy data. By using lexical processing and named entity recognition, developers can create high-speed, cost-effective pipelines that provide reliable inputs for large language models. 

The session emphasizes that while LLMs excel at complex reasoning and synthesis, classical methods ensure data integrity and enforce business logic. Ultimately, the material advocates for an orchestrated architecture that combines the precision of symbolic programming with the flexible understanding of generative AI.


{{< podcast src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/why_ai_agents_need_classical_nlp.m4a" title="Why AI Agents Need Classical NLP" >}}

{{< podcast src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/classical_nlp_guardrails_for_llm_agents.m4a" title="Classical NLP Guardrails for LLM Agents" >}}

### Presentation
 - [NLP and Text Processing](../../slides/slide-08-nlp-text-processing/)

### Notebooks
- [01_From_Raw_Text_to_Structured_Inputs](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/NLP-Textprocessing/notebooks/01_From_Raw_Text_to_Structured_Inputs.ipynb)
- [02_Lexical_Processing](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/NLP-Textprocessing/notebooks/02_Lexical_Processing.ipynb)
- [03_Grammars_and_Parsing](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/NLP-Textprocessing/notebooks/03_Grammars_and_Parsing.ipynb)
- [04_NER_and_POS_Tagging](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/NLP-Textprocessing/notebooks/04_NER_and_POS_Tagging.ipynb)
- [05_Text_Classification_Sentiment_Topic_Modeling](https://github.com/molnarai/BuildingGenerativeAIBusinessSolutions/blob/main/NLP-Textprocessing/notebooks/05_Text_Classification_Sentiment_Topic_Modeling.ipynb)

### Resources

| Package | Documentation | Description |
|---------|---------------|-------------|
| [re](https://pypi.org/project/regex/) | [re — Regular expression operations](https://docs.python.org/3/library/re.html) | Python standard library module for pattern matching with regular expressions. Used for extracting dates, amounts, emails, and IDs from text. |
| [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) | [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) | HTML/XML parser for navigating, searching, and extracting content from web pages. Used to strip noise (nav, ads, scripts) and extract clean text. |
| [nltk](https://pypi.org/project/nltk/) | [NLTK Documentation](https://www.nltk.org/) | Comprehensive natural language processing library. Used across notebooks for tokenization, stemming, lemmatization, POS tagging, grammars, WordNet, stop words, and VADER sentiment. |
| [nltk.tokenize](https://pypi.org/project/nltk/) | [nltk.tokenize API](https://www.nltk.org/api/nltk.tokenize.html) | Word and sentence tokenizers (`word_tokenize`, `sent_tokenize`) that handle contractions, abbreviations, and punctuation correctly. |
| [nltk.stem .PorterStemmer](https://pypi.org/project/nltk/) | [nltk.stem API](https://www.nltk.org/api/nltk.stem.html) | Rule-based suffix-stripping stemmer. Fast, moderate aggressiveness. Used for keyword matching and alert triggers. |
| [nltk.stem .SnowballStemmer](https://pypi.org/project/nltk/) | [nltk.stem API](https://www.nltk.org/api/nltk.stem.html) | Improved Porter variant with multi-language support. |
| [nltk.stem .LancasterStemmer](https://pypi.org/project/nltk/) | [nltk.stem API](https://www.nltk.org/api/nltk.stem.html) | Aggressive stemmer that strips more suffixes than Porter or Snowball. |
| [nltk.stem .WordNetLemmatizer](https://pypi.org/project/nltk/) | [nltk.stem API](https://www.nltk.org/api/nltk.stem.html) | Dictionary-based lemmatizer that reduces words to valid base forms (e.g., "geese" → "goose"). Requires POS tags for best results. |
| [nltk.corpus .wordnet](https://pypi.org/project/nltk/) | [WordNet Interface](https://www.nltk.org/howto/wordnet.html) | Lexical database of English providing synsets, synonyms, antonyms, hypernyms, and hyponyms. Used to build synonym lexicons for keyword expansion. |
| [nltk.corpus .stopwords](https://pypi.org/project/nltk/) | [NLTK Corpora](https://www.nltk.org/nltk_data/) | Curated lists of high-frequency, low-information words (179 English stop words) used to filter noise from text. |
| [nltk.sentiment .SentimentIntensityAnalyzer (VADER)](https://pypi.org/project/nltk/) | [VADER Sentiment](https://www.nltk.org/api/nltk.sentiment.vader.html) | Lexicon-based sentiment analyzer tuned for social media. Returns compound, positive, neutral, and negative scores. No training required. |
| [nltk.CFG / nltk.ChartParser](https://pypi.org/project/nltk/) | [nltk.parse API](https://www.nltk.org/api/nltk.parse.html) | Context-Free Grammar definition and chart parsing. Used to build deterministic command interpreters with parse trees. |
| [nltk.pos_tag](https://pypi.org/project/nltk/) | [nltk.tag API](https://www.nltk.org/api/nltk.tag.html) | Penn Treebank POS tagger using the averaged perceptron model. Labels words as NNP, VBD, JJ, etc. |
| [spacy](https://pypi.org/project/spacy/) | [spaCy Documentation](https://spacy.io/api) | Industrial-strength NLP library for tokenization, POS tagging, dependency parsing, NER, and lemmatization in a single pipeline call. |
| [en_core_web_sm](https://spacy.io/models/en#en_core_web_sm) | [spaCy English Models](https://spacy.io/models/en) | Small English pipeline model for spaCy (~12 MB). Includes tok2vec, tagger, parser, NER, and lemmatizer. Install with `python -m spacy download en_core_web_sm`. |
| [spacy.displacy](https://pypi.org/project/spacy/) | [displaCy Visualizer](https://spacy.io/usage/visualizers) | Built-in entity and dependency visualizer that renders inline in Jupyter notebooks. |
| [scikit-learn (sklearn)](https://pypi.org/project/scikit-learn/) | [scikit-learn Documentation](https://scikit-learn.org/stable/) | Machine learning library. Used for TF-IDF vectorization, logistic regression classification, LDA topic modeling, and evaluation metrics. |
| [sklearn .feature_extraction.text .TfidfVectorizer](https://pypi.org/project/scikit-learn/) | [TfidfVectorizer API](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) | Converts text to TF-IDF feature matrices. Supports stop words, n-grams, min/max document frequency thresholds. |
| [sklearn .feature_extraction.text .CountVectorizer](https://pypi.org/project/scikit-learn/) | [CountVectorizer API](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html) | Converts text to raw word-count matrices (bag of words). Used as input for LDA topic modeling. |
| [sklearn .linear_model .LogisticRegression](https://pypi.org/project/scikit-learn/) | [LogisticRegression API](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) | Linear classifier for text classification. Supports multi-class, outputs probabilities, and has inspectable coefficients for explainability. |
| [sklearn .decomposition .LatentDirichletAllocation](https://pypi.org/project/scikit-learn/) | [LDA API](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html) | Unsupervised topic model that discovers latent themes from a document-term matrix. |
<!-- | [sklearn.model_selection.train_test_split](https://pypi.org/project/scikit-learn/) | [train_test_split API](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) | Splits data into training and test sets with optional stratification. |
| [sklearn.metrics.classification_report](https://pypi.org/project/scikit-learn/) | [classification_report API](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html) | Generates precision, recall, F1, and support for each class in a classification task. | -->
<!-- | [numpy](https://pypi.org/project/numpy/) | [NumPy Documentation](https://numpy.org/doc/stable/) | Fundamental array computing library. Used for sorting model coefficients to identify top features. |
| [pandas](https://pypi.org/project/pandas/) | [pandas Documentation](https://pandas.pydata.org/docs/) | Data manipulation library. Used to display TF-IDF matrices as readable DataFrames. | -->