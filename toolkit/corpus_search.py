import json
import re
import argparse
from pathlib import Path

# ============================================================
# 0. define functions and command-line arguements
# ============================================================

# ------------------------------------------------------------
# define functions
# ------------------------------------------------------------

# function for loading corpus
def load_corpus(corpus_dir):

    corpus_dir = Path(corpus_dir)
    documents = []

    for file_path in sorted(corpus_dir.glob("*.json")):
        with file_path.open("r", encoding="utf-8") as file:
            document = json.load(file)
        documents.append(document)
    return documents

# function for keyword search
def keyword_search(documents, keyword, raw=False):

    results = []

    for document in documents:
        if raw:
            text = document["text"]

            if keyword in text:
                results.append({
                    "document_id": document["id"],
                    "keyword": keyword
                })

        else:
            tokens = document["filtered_tokens"]
            
            for i, token in enumerate(tokens):
                if token == keyword:
                    results.append({
                        "document_id": document["id"],
                        "position": i,
                        "token": token
                    })

    return results

# function for regular expression search
def regex_search(documents, pattern, raw=False):

    results = []
    regex = re.compile(pattern)

    for document in documents:
        if raw:
            text = document["text"]
            match = regex.search(text)

            if match:
                results.append({
                    "document_id": document["id"],
                    "match": match.group()
                })

        else:
            tokens = document["filtered_tokens"]

            for i, token in enumerate(tokens):
                if regex.search(token):
                    results.append({
                        "document_id": document["id"],
                        "position": i,
                        "token": token
                    })

    return results

# function for pos search
def pos_search(documents, pos_tag):

    results = []

    for document in documents:

        tokens = document["filtered_tokens"]

        for i, token_info in enumerate(tokens):

            if token_info["pos"] == pos_tag:
                results.append({
                    "document_id": document["id"],
                    "position": i,
                    "token": token_info["token"],
                    "pos": token_info["pos"]
                })

    return results

# function for printing search results
def print_results(results, title, limit=20):

    print("-" * 50)
    print(f"> {title}")
    print("-" * 50)
    print("Number of results:", len(results))

    for result in results[:limit]:
        print(result)

# ------------------------------------------------------------
# define command-line arguments
# ------------------------------------------------------------
parser = argparse.ArgumentParser(
    description="Search a corpus using keywords, regular expressions, or POS tags."
)

parser.add_argument(
    "--keyword",
    help="search for an exact keyword"
)

parser.add_argument(
    "--regex",
    help="search for tokens matching a regular expression"
)

parser.add_argument(
    "--pos",
    help="search for tokens with a specific POS tag | see 'pos_tagset.txt' for tags available"
)

parser.add_argument(
    "--raw",
    action="store_true",
    help="search the *raw* corpus instead of the *preprocessed* corpus"
)

parser.add_argument(
    "--show",
    type=int,
    default=20,
    metavar="N",
    help="number of results to display in the terminal (default: 20)"
)

args = parser.parse_args()

if args.raw and args.pos:
    parser.error("--pos cannot be used with --raw.")

if not any([args.keyword, args.regex, args.pos]):
    parser.error(
        "\n! Use at least one search option: --keyword, --regex, or --pos. "
        "\n! Use -h or --help for more information."
    )

# ============================================================
# 1. load preprocessed corpus
# ============================================================
if args.raw:
    corpus_dir = "data/raw/"
else:
    corpus_dir = "data/preprocessed/"

documents = load_corpus(corpus_dir)

print("-" * 50)
print("Corpus for keyword & regex search:", corpus_dir)
print("Corpus for POS search: data/pos_tagged/")
print("Number of documents:", len(documents))

# ============================================================
# 2. corpus search
# ============================================================
# ------------------------------------------------------------
# 2.1 keyword search
# ------------------------------------------------------------
keyword = args.keyword
keyword_results = []

if keyword:
    keyword_results = keyword_search(
        documents,
        keyword,
        raw=args.raw
    )

    print_results(
        keyword_results,
        f"Keyword search: {keyword}",
        limit=args.show
    )

# ------------------------------------------------------------
# 2.2 regular expression search
# ------------------------------------------------------------
pattern = args.regex
regex_results = []

if pattern:
    regex_results = regex_search(
        documents,
        pattern,
        raw=args.raw
    )

    print_results(
        regex_results,
        f"Regex search: {pattern}",
        limit=args.show
    )

# ------------------------------------------------------------
# 2.3 POS search
# ------------------------------------------------------------
pos_documents = load_corpus("data/pos_tagged")
pos_tag = args.pos
pos_results = []

if pos_tag:
    pos_documents = load_corpus("data/pos_tagged")
    pos_results = pos_search(
        pos_documents,
        pos_tag
    )

    print_results(
        pos_results,
        f"POS search: POS = {pos_tag}",
        limit=args.show
    )

# ============================================================
# 3. save search results
# ============================================================
results_dir = Path("data/results")
results_dir.mkdir(parents=True, exist_ok=True)

search_results = {
    "keyword_search": {
        "keyword": keyword,
        "frequency": len(keyword_results),
        "results": keyword_results
    },

    "regex_search": {
        "pattern": pattern,
        "frequency": len(regex_results),
        "results": regex_results
    },

    "pos_search": {
        "pos_tag": pos_tag,
        "frequency": len(pos_results),
        "results": pos_results
    }
}

output_file = (results_dir / "search_results.json")

with output_file.open("w", encoding="utf-8") as file:
    json.dump(
        search_results,
        file,
        ensure_ascii=False,
        indent=2
    )

print("-" * 50)
print("> Corpus search completed.")
print("> Search results saved to:", output_file)
print("-" * 50)