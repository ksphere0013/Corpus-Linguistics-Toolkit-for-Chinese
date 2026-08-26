import argparse
import json
import math
from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import rcParams  # for displaying Chinese characters in plots

# configure font for Chinese characters in plots
rcParams["font.sans-serif"] = ["Microsoft YaHei"]
rcParams["axes.unicode_minus"] = False

# ============================================================
# 0. define functions and command line arguments for analysis
# ============================================================

# ------------------------------------------------------------
# define functions
# ------------------------------------------------------------

# function for loading preprocessed JSON documents
def load_preprocessed_corpus(corpus_dir):

    corpus_dir = Path(corpus_dir)
    documents = []

    for file_path in sorted(corpus_dir.glob("*.json")):

        with file_path.open("r", encoding="utf-8") as file:
            document = json.load(file)
        documents.append(document)

    return documents

# function for extracting all tokens from the corpus
def get_all_tokens(documents):

    all_tokens = []

    for document in documents:
        all_tokens.extend(document["filtered_tokens"])

    return all_tokens

# function for calculating word frequency
def word_frequency(tokens):
    return Counter(tokens)

# function for calculating character frequency
def character_frequency(tokens):

    characters = []

    for word in tokens:
        for character in word:
            characters.append(character)

    return Counter(characters)

# function for plotting frequency distributions
def plot_frequencies(
    frequencies,
    title,
    x_label,
    output_file,
    top_n=40
):
    items = frequencies.most_common(top_n)
    labels = [item[0] for item in items]
    values = [item[1] for item in items]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values)
    plt.xlabel(x_label)
    plt.ylabel("Frequency")
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # save the figure
    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()
    plt.close()

# function for building adjacent bigram counts
def build_collocation_counts(tokens):
    words = tokens
    word_counts = Counter(words)
    bigram_counts = Counter()

    # count adjacent bigrams
    for i in range(len(words) - 1):
        pair = (words[i], words[i + 1])
        bigram_counts[pair] += 1
    return word_counts, bigram_counts

# function for calculating Mutual Information
def mutual_information(
    observed,
    freq1,
    freq2,
    total_bigrams
):
    if observed == 0:
        return 0
    
    expected = (freq1 * freq2) / total_bigrams

    if expected == 0:
        return 0
    
    return math.log2(observed / expected)

# function for calculating t-score
def t_score(
    observed,
    freq1,
    freq2,
    total_bigrams
):
    expected = (freq1 * freq2) / total_bigrams
    if observed == 0:
        return 0
    
    return (observed - expected) / math.sqrt(observed)

# function for calculating Dice coefficient
def dice_coefficient(
    observed,
    freq1,
    freq2
):
    denominator = freq1 + freq2
    if denominator == 0:
        return 0
    
    return (2 * observed) / denominator

# function for calculating log-likelihood
def log_likelihood(
    observed,
    freq1,
    freq2,
    total_bigrams
):
    if observed == 0:
        return 0
    expected = (freq1 * freq2) / total_bigrams
    if expected == 0:
        return 0
    
    return 2 * observed * math.log(observed / expected)

# function for all collocation analysis above
def collocation_analysis(
    tokens,
    min_frequency=5
):
    word_counts, bigram_counts = build_collocation_counts(tokens)

    # N = total number of bigrams
    total_bigrams = sum(bigram_counts.values())
    results = []

    for (word1, word2), observed in bigram_counts.items():
        # ignore low-frequency bigrams
        if observed < min_frequency:
            continue

        freq1 = word_counts[word1]
        freq2 = word_counts[word2]

        # calculate association measures
        mi = mutual_information(
            observed,
            freq1,
            freq2,
            total_bigrams
        )

        t = t_score(
            observed,
            freq1,
            freq2,
            total_bigrams
        )

        dice = dice_coefficient(
            observed,
            freq1,
            freq2
        )

        ll = log_likelihood(
            observed,
            freq1,
            freq2,
            total_bigrams
        )

        results.append({
            "word1": word1,
            "word2": word2,
            "frequency": observed,
            "word1_frequency": freq1,
            "word2_frequency": freq2,
            "MI": mi,
            "t_score": t,
            "Dice": dice,
            "log_likelihood": ll
        })

    return results


# ------------------------------------------------------------
# define command-line arguments
# ------------------------------------------------------------

parser = argparse.ArgumentParser(
    description="Run frequency and collocation analysis on preprocessed documents."
)
parser.add_argument(
    "--show",
    type=int,
    default=20,
    help="number of results to display and plot (default: 20)."
)

args = parser.parse_args()
show_n = args.show

# ============================================================
# 1. load data
# ============================================================

# load the preprocessed corpus
print("-" * 50)
documents = load_preprocessed_corpus("data/preprocessed")
print("Number of documents:", len(documents))

# collect all tokens
all_tokens = get_all_tokens(documents)
print("Total tokens:", len(all_tokens))

# ============================================================
# 2. frequency analysis
# ============================================================

# create directory for analysis results
results_dir = Path("data/results")
results_dir.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# 2.1 word frequency analysis
# ------------------------------------------------------------

word_freq = word_frequency(all_tokens)
print("Number of word types:", len(word_freq))
print("-" * 50)
print("1. frequency analysis")
print("-" * 50)
print("-" * 40)
print(f"> Top {show_n} most frequent words:")
print("-" * 40)

for word, frequency in word_freq.most_common(show_n):
    print(word, frequency)

# visualize word frequency
plot_frequencies(
    word_freq,
    f"Top {show_n} Most Frequent Words",
    "Words",
    results_dir / "word_frequency.png",
    top_n=show_n
)

# ------------------------------------------------------------
# 2.2 character frequency analysis
# ------------------------------------------------------------

char_freq = character_frequency(all_tokens)
print("-" * 40)
print(f"> Top {show_n} most frequent characters:")
print("-" * 40)

for character, frequency in char_freq.most_common(show_n):
    print(character, frequency)

# visualize character frequency
plot_frequencies(
    char_freq,
    f"Top {show_n} Most Frequent Characters",
    "Characters",
    results_dir / "character_frequency.png",
    top_n=show_n
)

# ------------------------------------------------------------
# 2.3 collocation analysis
# ------------------------------------------------------------

collocations = collocation_analysis(
    all_tokens,
    min_frequency=5
)
print("-" * 50)
print("2. collocation analysis")
print("-" * 50)

# 2.3.1 sort collocations by MI
collocations_by_mi = sorted(
    collocations,
    key=lambda x: x["MI"],
    reverse=True
)

print("-" * 30)
print(f"> Top {show_n} collocations by MI:")
print("-" * 30)

for result in collocations_by_mi[:show_n]:
    print(
        result["word1"],
        result["word2"],
        "freq=",
        result["frequency"],
        "MI=",
        round(result["MI"], 3)
    )

# 2.3.2 sort collocations by t-score
collocations_by_t = sorted(
    collocations,
    key=lambda x: x["t_score"],
    reverse=True
)

print("-" * 40)
print(f"> Top {show_n} collocations by t-score:")
print("-" * 40)

for result in collocations_by_t[:show_n]:
    print(
        result["word1"],
        result["word2"],
        "freq=",
        result["frequency"],
        "t-score=",
        round(result["t_score"], 3)
    )

# 2.3.3 sort collocations by Dice coefficient
collocations_by_dice = sorted(
    collocations,
    key=lambda x: x["Dice"],
    reverse=True
)

print("-" * 40)
print(f"> Top {show_n} collocations by Dice:")
print("-" * 40)

for result in collocations_by_dice[:show_n]:
    print(
        result["word1"],
        result["word2"],
        "freq=",
        result["frequency"],
        "Dice=",
        round(result["Dice"], 3)
    )

# 2.3.4 sort collocations by log-likelihood
collocations_by_ll = sorted(
    collocations,
    key=lambda x: x["log_likelihood"],
    reverse=True
)

print("-" * 40)
print(f"> Top {show_n} collocations by log-likelihood:")
print("-" * 40)

for result in collocations_by_ll[:show_n]:
    print(
        result["word1"],
        result["word2"],
        "freq=",
        result["frequency"],
        "LL=",
        round(
            result["log_likelihood"],
            3
        )
    )

# ============================================================
# 3. save results
# ============================================================

# save all collocation results
output_file = results_dir / "collocations.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(
        collocations,
        file,
        ensure_ascii=False,
        indent=2
    )

print("-" * 50)
print("> Frequency analysis completed.")
print("Collocation results saved to:", output_file)

# save rankings by each statistical measure
ranked_results = {
    "MI": collocations_by_mi,
    "t_score": collocations_by_t,
    "Dice": collocations_by_dice,
    "log_likelihood": collocations_by_ll
}

ranked_output_file = results_dir / "collocations_ranked.json"

with ranked_output_file.open("w", encoding="utf-8") as file:
    json.dump(
        ranked_results,
        file,
        ensure_ascii=False,
        indent=2
    )

print("Ranked collocation results saved to:", ranked_output_file)
print("-" * 50)