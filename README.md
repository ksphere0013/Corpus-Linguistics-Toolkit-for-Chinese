# Corpus Linguistics Toolkit for Chinese


## Project Overview 
text

## Corpus Description
text

### Corpus License
text    

## Data Collection Approach 
text

## System Architecture
text

## Usage Instruction with Example Commands

### 1. preprocessing (POS tagging included)
optionally with document filtering based on metadata parameter(s):

```bash
python -m Toolkit.preprocessing --license "CC BY-NC-SA 3.0" --genre "Online News Article"
```

Note: if your parameter has white space, put it in quotation marks "".

### 2. frequency analysis

```bash
python -m Toolkit.frequency
```

### 3. corpus analysis

```bash
python -m Toolkit.corpus_analysis
```

By default, it shows only basic document info and TTR result.

Use `--kwic` to include concordance analysis.

```bash
python -m Toolkit.corpus_analysis --kwic 女性
```

### 4. corpus search
```bash
python -m Toolkit.corpus_search
```
### 5. N-gram analysis
```bash
python -m Toolkit.ngram
```

## Example outputs 
text

## Challenges Faced
text