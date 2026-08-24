import argparse
import json
from collections import Counter
from pathlib import Path


# ============================================================
# 0. define functions and command line arguments for analysis
# ============================================================

# ------------------------------------------------------------
# define functions
# ------------------------------------------------------------

# function for loading preprocessed JSON documents
def load_corpus(corpus_dir):

    corpus_dir = Path(corpus_dir)
    documents = []

    for file_path in sorted(corpus_dir.glob("*.json")):

        with file_path.open("r", encoding="utf-8") as file:
            document = json.load(file)

        documents.append(document)

    return documents


# function for extracting all filtered tokens
def get_all_tokens(documents):

    all_tokens = []

    for document in documents:
        all_tokens.extend(document["filtered_tokens"])

    return all_tokens


# function for generating n-grams
def generate_ngrams(tokens, n):

    ngrams = []

    for i in range(len(tokens) - n + 1):

        ngram = tuple(tokens[i:i + n])

        ngrams.append(ngram)

    return ngrams


# function for calculating n-gram frequencies
def calculate_ngram_frequency(tokens, n):

    ngrams = generate_ngrams(tokens, n)

    return Counter(ngrams)


# function for printing n-gram results
def print_ngram_results(frequencies, n, limit):

    if n == 1:
        title = "Unigram"

    elif n == 2:
        title = "Bigram"

    elif n == 3:
        title = "Trigram"

    else:
        title = f"{n}-gram"

    print("-" * 40)
    print(f"> Top {limit} {title} frequencies:")
    print("-" * 40)

    for ngram, frequency in frequencies.most_common(limit):

        print(
            " ".join(ngram),
            "freq=",
            frequency
        )


# ------------------------------------------------------------
# define command-line arguments
# ------------------------------------------------------------

parser = argparse.ArgumentParser(
    description="Run n-gram frequency analysis on preprocessed documents."
)

parser.add_argument(
    "--top",
    type=int,
    default=20,
    help="number of top n-grams to display and save (default: 20)"
)

args = parser.parse_args()
top_n = args.top


# ============================================================
# 1. load data
# ============================================================

# load preprocessed documents
print("-" * 50)
documents = load_corpus("data/preprocessed")
print("Number of documents:", len(documents))

# collect all filtered tokens
all_tokens = get_all_tokens(documents)
print("Total tokens:", len(all_tokens))


# ============================================================
# 2. n-gram analysis
# ============================================================

# ------------------------------------------------------------
# 2.1 unigram analysis
# ------------------------------------------------------------

unigram_frequencies = calculate_ngram_frequency(
    all_tokens,
    1
)

print_ngram_results(
    unigram_frequencies,
    1,
    limit=top_n
)


# ------------------------------------------------------------
# 2.2 bigram analysis
# ------------------------------------------------------------

bigram_frequencies = calculate_ngram_frequency(
    all_tokens,
    2
)

print_ngram_results(
    bigram_frequencies,
    2,
    limit=top_n
)


# ------------------------------------------------------------
# 2.3 trigram analysis
# ------------------------------------------------------------

trigram_frequencies = calculate_ngram_frequency(
    all_tokens,
    3
)

print_ngram_results(
    trigram_frequencies,
    3,
    limit=top_n
)


# ============================================================
# 3. save results
# ============================================================

results_dir = Path("data/results")

results_dir.mkdir(parents=True, exist_ok=True)


ngram_results = {

    "unigram": [
        {
            "ngram": list(ngram),
            "frequency": frequency
        }
        for ngram, frequency
        in unigram_frequencies.most_common(top_n)
    ],

    "bigram": [
        {
            "ngram": list(ngram),
            "frequency": frequency
        }
        for ngram, frequency
        in bigram_frequencies.most_common(top_n)
    ],

    "trigram": [
        {
            "ngram": list(ngram),
            "frequency": frequency
        }
        for ngram, frequency
        in trigram_frequencies.most_common(top_n)
    ]

}


output_file = results_dir / "ngram_results.json"


with output_file.open("w", encoding="utf-8") as file:

    json.dump(
        ngram_results,
        file,
        ensure_ascii=False,
        indent=2
    )


print("-" * 50)
print("> N-gram analysis completed.")

print("N-gram results saved to:", output_file)

print("-" * 50)