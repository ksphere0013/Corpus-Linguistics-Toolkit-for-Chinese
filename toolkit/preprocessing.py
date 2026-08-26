import json
import re
import jieba
import jieba.posseg as pseg
import argparse
from pathlib import Path

# ============================================================
# 0. define functions and arguments for preprocessing
# ============================================================

# ------------------------------------------------------------
# define functions
# ------------------------------------------------------------

# function for loading all JSON documents from a specified directory
def load_corpus(corpus_dir):

    corpus_dir = Path(corpus_dir)
    documents = []

    for file_path in sorted(corpus_dir.glob("*.json")): # get all JSON files and sort by name

        with file_path.open("r", encoding="utf-8") as file:

            document = json.load(file) # load JSON content into Python dictionary

        documents.append(document)

    return documents


# function for filtering documents based on metadata
def filter_documents(
    documents,
    source=None,
    author=None,
    topic=None,
    genre=None,
    license=None
):

    filtered = []

    for document in documents:

        metadata = document["metadata"]

        if source is not None:
            if source not in metadata.get("source"):
                continue

        if author is not None:
            if author not in metadata.get("author"):
                continue

        if topic is not None:
            if topic not in metadata.get("topic"):
                continue

        if genre is not None:
            if genre not in metadata.get("genre"):
                continue

        if license is not None:
            if license not in metadata.get("license"):
                continue

        filtered.append(document)

    return filtered


# function for splitting text into sentences
def sentence_segment(text):

    # split text by punctuation marks and newlines
    sentences = re.split(r'(?<=[。！？!?])|[\r\n]+', text)

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    return sentences


# function for tokenizing and POS-tagging text using jieba
def tokenize(text):

    tokens = []

    for word, pos in pseg.cut(text):
        tokens.append({"token": word, "pos": pos})

    return tokens


# function for removing punctuation from a list of tokens
def remove_punctuation(tokens):

    cleaned_tokens = []

    for token in tokens:

        if re.fullmatch(
            r'[\W_]+',
            token["token"],
            flags=re.UNICODE
        ):
            continue

        cleaned_tokens.append(token)

    return cleaned_tokens


# function for loading stopwords from a JSON file
def load_stopwords(path):

    path = Path(path)

    with path.open("r", encoding="utf-8") as f:

        stopwords = json.load(f)

    return set(stopwords)


# function for removing stopwords from a list of tokens
def remove_stopwords(tokens, stopwords):

    return [
        token
        for token in tokens
        if token["token"] not in stopwords
    ]


# function for converting POS-tagged tokens into a list with only token strings
# for the convenience of following analysis
def extract_tokens(tokens):

    return [
        token["token"]
        for token in tokens
    ]


# function for the complete preprocessing pipeline
def preprocess_text(text, stopwords):

    sentences = sentence_segment(text)

    # tokenize and POS-tag 
    tagged_tokens = tokenize(text)

    # remove punctuation
    tagged_tokens = remove_punctuation(tagged_tokens)

    # remove stopwords
    filtered_tagged_tokens = remove_stopwords(
        tagged_tokens,
        stopwords
    )

    # create token-only lists
    tokens = extract_tokens(tagged_tokens)
    filtered_tokens = extract_tokens(filtered_tagged_tokens)

    return {
        "sentences": sentences,
        "tokens": tokens,
        "filtered_tokens": filtered_tokens,
        "tagged_tokens": tagged_tokens,
        "filtered_tagged_tokens": filtered_tagged_tokens
    }

# ------------------------------------------------------------
# define command-line arguments
# ------------------------------------------------------------

parser = argparse.ArgumentParser(
    description="Preprocess the raw data. Optionally filter documents by metadata."
)

parser.add_argument(
    "--source",
    help="filter documents by keyword in [source]"
)

parser.add_argument(
    "--author",
    help="filter documents by keyword in [author]"
)

parser.add_argument(
    "--topic",
    help="filter documents by keyword in [topic]"
)

parser.add_argument(
    "--genre",
    help="filter documents by [genre]"
)

parser.add_argument(
    "--license",
    dest="license_name",
    help="filter documents by [license]"
)

args = parser.parse_args()

# ============================================================
# 1. load data
# ============================================================

# load and filter the corpus
documents = load_corpus("data/raw")
print("-" * 50)
print("> Number of documents:", len(documents))

documents = filter_documents(
    documents,
    source=args.source,
    author=args.author,
    topic=args.topic,
    genre=args.genre,
    license=args.license_name
)

print("-" * 50)
print("> Filtering criteria:")

if not any([
    args.source,
    args.author,
    args.topic,
    args.genre,
    args.license_name
]):
    print("[None]")
else:

    if args.source:
        print("| Source:", args.source)

    if args.author:
        print("| Author:", args.author)

    if args.topic:
        print("| Topic:", args.topic)

    if args.genre:
        print("| Genre:", args.genre)

    if args.license_name:
        print("| License:", args.license_name)

print("-" * 50)
print("> Number of documents after filtering:", len(documents))

# load stopwords
print("-" * 50)
stopwords = load_stopwords("data/stopwords.json")
print(f"> {len(stopwords)} stopwords loaded.")
print("Stopwords:", stopwords)

# ============================================================
# 2. preprocess the documents
# ============================================================

print("-" * 50)
print("> Tokenizing...")

# create lists for 2 versions of preprocessed documents: 
# token-only and POS-tagged
preprocessed_documents = []
pos_tagged_documents = []

for document in documents:

    result = preprocess_text(document["text"], stopwords)

    # Version 1: token-only documents
    preprocessed_document = {
        "id": document["id"],
        "metadata": document["metadata"],
        "sentences": result["sentences"],
        "tokens": result["tokens"],
        "filtered_tokens": result["filtered_tokens"]
    }
    preprocessed_documents.append(preprocessed_document)

    # Version 2: POS-tagged documents
    pos_tagged_document = {
        "id": document["id"],
        "metadata": document["metadata"],
        "sentences": result["sentences"],
        "tokens": result["tagged_tokens"],
        "filtered_tokens": result["filtered_tagged_tokens"]
    }
    pos_tagged_documents.append(pos_tagged_document )


# calculate total tokens and total filtered tokens
total_tokens = sum(
    len(document["tokens"])
    for document in preprocessed_documents
)

total_filtered_tokens = sum(
    len(document["filtered_tokens"])
    for document in preprocessed_documents
)

print("> Tokenization compeleted.")
print("Total tokens:", total_tokens)
print("Total tokens after stopword removal:", total_filtered_tokens)


# ============================================================
# 3. save preprocessed documents to files
# ============================================================

# version 1: token-only documents
preprocessed_dir = Path("data/preprocessed")
preprocessed_dir.mkdir(parents=True, exist_ok=True)

for document in preprocessed_documents:

    output_file = (preprocessed_dir/ f"{document['id']}.json")

    with output_file.open("w", encoding="utf-8") as f:

        json.dump(
            document,
            f,
            ensure_ascii=False,
            indent=2
        )


# version 2: POS-tagged documents
pos_tagged_dir = Path("data/pos_tagged")
pos_tagged_dir.mkdir(parents=True, exist_ok=True)

for document in pos_tagged_documents:

    output_file = (pos_tagged_dir/ f"{document['id']}.json")

    with output_file.open("w", encoding="utf-8") as f:

        json.dump(
            document,
            f,
            ensure_ascii=False,
            indent=2
        )

print("-" * 50)
print("> Preprocessing completed.")
print("Token-only documents saved to:", preprocessed_dir)
print("POS-tagged documents saved to:", pos_tagged_dir)
print("-" * 50)
