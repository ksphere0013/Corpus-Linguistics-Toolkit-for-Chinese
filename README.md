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
> **Note:**
> The `crawler.py` is included in the toolkit for reference only and may require adaptation to different website layouts.

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

The preprocessing module reads the raw JSON corpus stored in `data/raw/`, generates token-only data for general corpus analysis, saved in `data/preprocessed/`, and POS-tagged data, saved in `data/pos_tagged/`. 

The *preprocessed* and *pos_tagged* data can then be independently processed by the analysis modules. Analysis results, including frequency tables, collocations,
search results, KWIC results, and N-gram statistics, are stored in `data/results/`.

> **Note:**
> POS tagging is included in the preprocessing module because the chosen tokenizer `jieba` (a lightweight and widely used tokenizer for Chinese language) conduct both tokenization and POS tagging through its `jieba.posseg` module at the same time.

## **5. Usage Instruction with Example Commands and Output**
See `installation.md` for installation instrucion.

### **General**
After installation, in your terminal, change directory to where your `data` folder is.
For example, the path of my data folder is `A:\test\data\`, so I do:
```bash
cd A:\test\
```

Then, you can run each module in the toolkit from the same directory.

To use each module, run:
```bash
python -m toolkit.[module_name]
```
For example, 
```bash
python -m toolkit.preprocessing
```
For each module, use `-h` or `--help` to see instructions for different options. 
```bash
python -m toolkit.preprocessing [-h]
```
Some modules require at least one option to run. See examples below.

### **Preprocessing (POS tagging included)**

By default, all documents in `data/raw/` will be preprocessed if you run this:

```bash
python -m toolkit.preprocessing
```

You can use options to filter your data. For example:

```bash
python -m toolkit.preprocessing --license "CC BY-NC-SA 3.0" --genre "Online News Article" --topic 中国
```

<details>
<summary> click here to show example output </summary>

```text
--------------------------------------------------
> Number of documents: 159
--------------------------------------------------
> Filtering criteria:
| Topic: 中国
| Genre: Online News Article
| License: CC BY-NC-SA 3.0
--------------------------------------------------
> Number of documents after filtering: 12
--------------------------------------------------
> 89 stopwords loaded.
Stopwords: {'让', '一种', '还', '会', '从', '地', '最', '已经', '它', '其实', '像', '年', '多', '什么', '称', '但', '把', '于', '被', '到', '对', '那', '人', '这些', '没有', '要', '或者', '这', '很多', '却', '能', '不', '一些', '下', '之', '以', '中', '上', '和', '等', '而', '一', '其', '这种', '可能', '了', '这个', '日', '后', '或', '做', '已', '向', '甚至', '时', '去', '一个', '就是', '与', '的', '说', '也', '包括', '着', '很', '个', '都', '又', '这样', '但是', '是', '更', '可以', '并', '在', '因为', '通过', '不是', '有', '来', '该', '还是', '以及', '为', '月', '将', '就', '里', '给'}
--------------------------------------------------
> Tokenizing...
Building prefix dict from the default dictionary ...
Loading model from cache C:\Users\ma188\AppData\Local\Temp\jieba.cache
Loading model cost 0.726 seconds.
Prefix dict has been built successfully.
> Tokenization compeleted.
Total tokens: 23342
Total tokens after stopword removal: 17045
--------------------------------------------------
> Preprocessing completed.
Token-only documents saved to: data\preprocessed
POS-tagged documents saved to: data\pos_tagged
--------------------------------------------------
```

</details> 

> **Notes**: 
> 1. Here, filtering uses partial matching rather than exact matching.
> 2. If your option parameters have white space, put them in quotation marks ("").
> 3. The stopword list used in this preprocessing module is stored in `data/stopwords.json`. You can change the list according to your purpose.

### **Frequency Analysis**

By default, the top 20 results are displayed in the terminal for all frequency and collocation analyses.

You can change the number of displayed results by adding `--top [NUMBER]` to your command. For example:

```bash
python -m toolkit.frequency --top 5
```
The `--top` option only affects the number of results displayed in the terminal and does not affect the analysis results; the complete results are always saved in the corresponding JSON files regardless of this setting.

<details>
<summary> click here to show example output </summary>

```text
--------------------------------------------------
Number of documents: 159
Total tokens: 248311
Number of word types: 29995
--------------------------------------------------
1. frequency analysis
--------------------------------------------------
----------------------------------------
> Top 5 most frequent words:
----------------------------------------
中国 2935
我 1887
我们 1253
报告 1031
你 1028
----------------------------------------
> Top 5 most frequent characters:
----------------------------------------
国 6526
2 5326
一 4792
中 4657
人 4330
--------------------------------------------------
2. collocation analysis
--------------------------------------------------
------------------------------
> Top 5 collocations by MI:
------------------------------
Safeguard Defenders freq= 5 MI= 15.6
叶 丰华 freq= 5 MI= 15.6
谍龟 谍鱼 freq= 5 MI= 15.6
Lingua Sinica freq= 5 MI= 15.6
赛默 飞世尔 freq= 5 MI= 15.6
----------------------------------------
> Top 5 collocations by t-score:
----------------------------------------
中国 数字 freq= 375 t-score= 19.057
数字 时代 freq= 336 t-score= 18.278
我 觉得 freq= 307 t-score= 17.321
报告 指出 freq= 140 t-score= 11.659
户 晨风 freq= 136 t-score= 11.655
----------------------------------------
> Top 5 collocations by Dice:
----------------------------------------
菲尔 兹 freq= 12 Dice= 1.0
瓦赫坦 戈夫 freq= 22 Dice= 1.0
叶甫盖 尼 freq= 7 Dice= 1.0
Safeguard Defenders freq= 5 Dice= 1.0
Wi Fi freq= 7 Dice= 1.0
----------------------------------------
> Top 5 collocations by log-likelihood:
----------------------------------------
数字 时代 freq= 336 LL= 3935.071
中国 数字 freq= 375 LL= 3106.74
我 觉得 freq= 307 LL= 2745.177
户 晨风 freq= 136 LL= 2006.317
404 文库 freq= 133 LL= 1828.399
--------------------------------------------------
> Frequency analysis completed.
> Collocation results saved to: data\results\collocations.json
> Ranked collocation results saved to: data\results\collocations_ranked.json
--------------------------------------------------
```

</details> 

### **Corpus Analysis**

By default, it shows only the TTR result. To perform concordance and KWIC analysis, use `--kwic` followed by a keyword. 

If you use `--kwic`, the terminal displays the top 20 KWIC results by default. You can change the number of displayed results using `--top`. 

Example:

```bash
python -m toolkit.corpus_analysis --kwic 女性 --top 5
```
The --top option only affects the number of results displayed in the terminal; complete concordance and KWIC results are saved to the corresponding JSON files regardless of this setting.

<details>
<summary> click here to show example output </summary>

```text
------------------------------
Number of documents: 159
------------------------------
> Token-Type Ratio (TTR)
------------------------------
Tokens: 248311
Types: 29995
TTR: 0.121
------------------------------
> Concordance Analysis
------------------------------
Keyword: 女性
Number of occurrences: 220
KWIC results:
--------------------------------------------------------------------------------
发生 父系社会 反而 全部 发生              女性          解放 时代 载人 航天 互联网
互联网 人工智能 重大 科技进步 发生           女性          地位 不断 提高 原有 性别
社交 软件 群组 针对 德华                女性          实施 系统性 迷奸 偷拍 传播
参与 宣传 一位 年轻 维吾尔族              女性          指示 回去 你 美好 经历
由此 成为 该奖 历史 第三位               女性          得主 二人 曾 北京大学 2007
--------------------------------------------------------------------------------
> Corpus analysis completed.
Concordance results saved to: data\results\concordance_results.json
KWIC results saved to: data\results\kwic_results.json
--------------------------------------------------------------------------------
```

</details> 

### **N-gram Analysis**

By default, the top 20 results are displayed in the terminal for unigram, bigram, and trigram analyses.

You can change the number of displayed results by adding `--top [NUMBER]` to your command. For example:

```bash
python -m toolkit.ngram
```

<details>
<summary> click here to show example output </summary>

```text

```

</details> 

### **Corpus Search**
```bash
python -m toolkit.corpus_search
```

<details>
<summary> click here to show example output </summary>

```text

```

</details> 



## **6. Challenges Faced**
- 一开始用request访问post archive，得到403 error，于是改用selenium
