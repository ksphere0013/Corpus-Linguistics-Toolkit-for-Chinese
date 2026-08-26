# **Corpus Linguistics Toolkit for Chinese**

## **1. Project Overview**
This project is a corpus linguistics toolkit written in Python for the analysis of Chinese corpora. It offers tools for corpus corpus preprocessing, corpus search, frequency analysis, collocation analysis, concordance/KWIC analysis and n-gram analysis.

## **2. Data Collection Approach**

The corpus was collected from the [China Digital Times (CDT)](https://chinadigitaltimes.net/chinese/) archive.

The crawler uses `Selenium` to access the CDT archive pages and collect article URLs, and `BeautifulSoup` to parse individual article pages. In the current implementation, URLs are collected from the first five archive pages. Articles without author information are excluded.

For each article, the crawler extracts the following metadata:

- `title`
- `source`
- `url`
- `author`
- `published`
- `genre`
- `topic`
- `copyright`
- `license`

The publication date is normalised to the `YYYY-MM-DD` format. The genre is recorded as `Online News Article`. When no topic can be extracted, the topic is recorded as `Unknown`.

The main article content is extracted from the `<article>` element, using its `h2`, `h3`, and `p` elements. Page-level metadata such as “所在分类(Category)” and “标签(Tag)”, as well as the “相关阅读” (Related Readings) section, are excluded from the corpus text.

`OpenCC` is used to convert Traditional Chinese characters, if any, to Simplified Chinese characters.

Each article is stored as a separate UTF-8 JSON file in `data/raw/`, with the article text and metadata stored separately. For example:

```json
{
  "id": "cdt_0149",
  "text": "...",
  "metadata": {
    "title": "...",
    "source": "China Digital Times",
    "url": "...",
    "author": "中国数字时代",
    "published": "2026-07-29",
    "genre": "Online News Article",
    "topic": "...",
    "copyright": "China Digital Times",
    "license": "CC BY-NC-SA 3.0"
  }
}
```

> *The `crawler.py` is provided in the toolkit for reference only and may require adaptation to different website layouts.*

## **3. Corpus Description**

The sample corpus consists of 159 Chinese-language online news articles collected from China Digital Times (CDT).

The corpus contains:

- **Documents:** 159
- **Tokens before stopword removal:** 340,277
- **Tokens after stopword removal:** 248,311

Each document is stored as an individual JSON file. The corpus contains both article text and structured metadata, including title, source, URL, author, publication date, genre, topic, copyright holder, and license.

The original content is licensed by China Digital Times under the [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License (CC BY-NC-SA 3.0)](https://creativecommons.org/licenses/by-nc-sa/3.0/). The original copyright and licensing information is preserved in the metadata of each document.

The corpus data is provided as a sample dataset for research and educational purposes. Users should comply with the terms of the original CC BY-NC-SA 3.0 license when using or redistributing the corpus data.

## **4. System Architecture**

The toolkit is organized as a modular command-line pipeline. Each module
performs a specific corpus-processing or analysis task and operates on
JSON-formatted corpus data.

The overall workflow is:

```mermaid
flowchart TD
    C[data/raw/]

    C --> D[preprocessing.py]

    D --> E[data/preprocessed/]
    D --> F[data/pos_tagged/]

    E --> G[frequency.py]
    E --> H[corpus_analysis.py]
    E --> I[ngram.py]
    E --> J[corpus_search.py]

    F --> J

    G --> K[data/results/]
    H --> K
    I --> K
    J --> K

    classDef python fill:#E8EEF2,stroke:#526777,stroke-width:2px,color:#263640;
    classDef data fill:#F5F1E8,stroke:#9A8C70,stroke-width:2px,color:#4A4338;

    class D,G,H,I,J python;
    class C,E,F,K data;
```

### **Main Components**

- **`preprocessing.py`** – performs sentence segmentation, tokenisation,
  punctuation removal, stopword removal, and POS tagging. It generates
  both token-only and POS-tagged versions of the corpus.
- **`frequency.py`** – performs word and character frequency analysis and
  collocation analysis using statistical association measures.
- **`corpus_analysis.py`** – provides basic corpus information, TTR,
  concordance generation, and KWIC analysis.
- **`corpus_search.py`** – supports keyword, regular expression, and
  pos-based searches.
- **`ngram.py`** – performs unigram, bigram, and trigram analysis.


### **Data Flow**

The `preprocessing` module reads the raw JSON corpus stored in `data/raw/`, generates token-only data for general corpus analysis, saved in `data/preprocessed/`, and POS-tagged data, saved in `data/pos_tagged/`. 

> *POS tagging is included in the preprocessing module because the chosen tokenizer `jieba` (a lightweight and widely used tokenizer for Chinese language) conduct both tokenization and POS tagging through its `jieba.posseg` module at the same time.*

The *preprocessed* and *pos_tagged* data can then be independently processed by the analysis modules. Analysis results, including frequency tables, collocations,
search results, KWIC results, and N-gram statistics, are stored in `data/results/`.

## **5. Usage Instruction with Example Commands and Output**

### **Preprocessing (POS tagging included)**
optionally with document filtering based on metadata parameter(s):

```bash
python -m Toolkit.preprocessing --license "CC BY-NC-SA 3.0" --genre "Online News Article"
```

> *Note: If your parameter has white space, put it in quotation marks ("").*

### **Frequency Analysis**

```bash
python -m Toolkit.frequency
```

### **Corpus Analysis**

```bash
python -m Toolkit.corpus_analysis
```

<details>
<summary> Show example output: </summary>

```text
Token count: 340277
Type count: 23681
TTR: 0.13
```

</details> 

By default, it shows only basic document info and TTR result.
To include concordance analysis, use `--kwic`.

```bash
python -m Toolkit.corpus_analysis --kwic 女性
```

### **Corpus Search**
```bash
python -m Toolkit.corpus_search
```
### **N-gram Analysis**
```bash
python -m Toolkit.ngram
```

## **6. Challenges Faced**
text
