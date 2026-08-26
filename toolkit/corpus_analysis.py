import json
import argparse
from pathlib import Path

# ============================================================
# 0. define functions and arguments for corpus analysis
# ============================================================

# ------------------------------------------------------------
# define functions
# ------------------------------------------------------------

# function for loading preprocessed documents
def load_preprocessed_corpus(corpus_dir):

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


# function for calculating Token-Type Ratio (TTR)
def calculate_ttr(tokens):

    token_count = len(tokens)
    type_count = len(set(tokens))

    if token_count == 0:
        return 0

    return type_count / token_count


# function for generating concordance lines
def generate_concordance(tokens, keyword, window_size=5):

    concordance = []

    for i, token in enumerate(tokens):

        if token != keyword:
            continue

        left_start = max(0, i - window_size)

        right_end = min(len(tokens), i + window_size + 1)

        left_context = tokens[left_start:i]

        right_context = tokens[i + 1:right_end]

        concordance.append({
            "left": left_context,
            "keyword": token,
            "right": right_context
        })

    return concordance


# function for generating KWIC (Key Word in Context) from concordance results
def generate_kwic(concordance):

    kwic_results = []

    for result in concordance:

        left = " ".join(result["left"])

        keyword = result["keyword"]

        right = " ".join(result["right"])

        kwic_results.append({
            "left": left,
            "keyword": keyword,
            "right": right
        })

    return kwic_results


# function for printing KWIC lines
def print_kwic(kwic_results,keyword):

    print(f"KWIC results:")

    print("-" * 80)

    for result in kwic_results:

        print(
            f"{result['left']:20} "
            f"{result['keyword']:^20} "
            f"{result['right']}"
        )

    print("-" * 80)

# ------------------------------------------------------------
# define command-line arguments
# ------------------------------------------------------------

parser = argparse.ArgumentParser(
    description="Perform TTR analysis, and concordance analysis if called, for preprocessed corpus."
)

parser.add_argument(
    "--kwic",
    metavar="KEYWORD",
    help="generate concordance and KWIC analysis for a keyword"
)

parser.add_argument(
    "--top",
    type=int,
    default=20,
    metavar="N",
    help="number of KWIC results to display in the terminal (default: 20)"
)

args = parser.parse_args()

# ============================================================
# 1. load data
# ============================================================

# load the preprocessed corpus
print("-" * 30)
documents = load_preprocessed_corpus("data/preprocessed")
print("Number of documents:", len(documents))

# collect all filtered tokens
all_tokens = get_all_tokens(documents)


# ============================================================
# 2. corpus analysis
# ============================================================

# ------------------------------------------------------------
# 2.1 calculate TTR
# ------------------------------------------------------------

ttr = calculate_ttr(all_tokens)
token_count = len(all_tokens)
type_count = len(set(all_tokens))

print("-" * 30)
print("> Token-Type Ratio (TTR)")
print("-" * 30)

print("Tokens:", token_count)   
print("Types:",type_count)
print(f"TTR: {ttr:.3f}") # show TTR rounded to three decimal places

# ------------------------------------------------------------
# 2.2 concordance analysis
# ------------------------------------------------------------

print("-" * 30)
print("> Concordance Analysis")
print("-" * 30)

if not args.kwic:
    parser.error("\n! Use --kwic for concordance analysis.")

if args.kwic:

    keyword = args.kwic 

    concordance = generate_concordance(
        all_tokens,
        keyword,
        window_size=5
    )

    print("Keyword:", keyword)
    print("Number of occurrences:", len(concordance))

# ------------------------------------------------------------
# 2.3 KWIC analysis
# ------------------------------------------------------------

    kwic_results = generate_kwic(concordance)

    # print first 20 KWIC results
    print_kwic(kwic_results[:args.top], keyword)


# ============================================================
# 3. Save results
# ============================================================

    results_dir = Path("data/results")
    results_dir.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# 3.1 save concordance results
# ------------------------------------------------------------

    concordance_output_file = (results_dir / "concordance_results.json")

    with concordance_output_file.open("w", encoding="utf-8") as file:

        json.dump(
            {
                "keyword": keyword,
                "window_size": 5,
                "frequency": len(concordance),
                "results": concordance
            },
            file,
            ensure_ascii=False,
            indent=2
        )

    print("> Corpus analysis completed.")
    print("Concordance results saved to:", concordance_output_file)


# ------------------------------------------------------------
# 3.2 save KWIC results
# ------------------------------------------------------------

    kwic_output_file = (results_dir/ "kwic_results.json")

    with kwic_output_file.open("w",encoding="utf-8") as file:

        json.dump(
            {
                "keyword": keyword,
                "window_size": 5,
                "frequency": len(kwic_results),
                "results": kwic_results
            },
            file,
            ensure_ascii=False,
            indent=2
        )

    print("KWIC results saved to:", kwic_output_file)
    print("-" * 80)