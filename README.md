# Corpus Linguistics Toolkit for Chinese


## Project Overview 


## Corpus Description

### Corpus License
    

## Data Collection Approach 


## System Architecture


## Usage Instruction with Example Commands

 1. preprocessing (POS tagging included); 
    optionally with document filtering based on metadata parameter(s):
    ```
    python -m Toolkit.preprocessing --license "CC BY-NC-SA 3.0" --genre "Online News Article"
    ```
    note: if your parameter has white space, put it in quotation marks "".
 
 2. frequency analysis
    ```
    python -m Toolkit.frequency
    ```

 3. corpus analysis
    ```
    python -m Toolkit.corpus_analysis
    ```
    By default, it shows only basic document info and TTR result.
    
    Use --kwic to include concordance analysis.
    ```
    python -m Toolkit.corpus_analysis --kwic 女性
    ```

 4. corpus search
    regex 例子

 5. N-gram analysis

## Example outputs 


## Challenges Faced