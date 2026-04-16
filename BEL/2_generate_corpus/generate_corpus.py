import re
import json
import os
from urllib.parse import unquote
import pandas as pd
import spacy
nlp = spacy.load("nl_core_news_sm", disable=["tagger", "parser", "ner", "lemmatizer"])
link_re = re.compile(r'<a href="([^"]+)">([^<]+)</a>')

# Build a map from the article titles to their cui
def build_title_map(path):
    df = pd.read_json(path, lines=True)
    titles = (
        df["article"]
        .str.rsplit("/", n=1).str[-1]
        .map(unquote)
        .str.replace("_", " ", regex=False)
    )
    return dict(zip(titles, df["cui"]))

# Normalize article title
def normalize_title(raw, mapping):
    title = unquote(raw.split("#")[0]).replace("_", " ").strip()
    variants = [
        title,
        title.lower(),
        title.capitalize(),
        re.sub(r"\s*\(.*?\)", "", title).strip()
    ]
    for v in variants:
        if v in mapping:
            return mapping[v]
    return None

# Go from a sentence to the sentence with their mentions where the links are replaced by the anchor text
def parse_sentence(sent, mapping):
    annotations = []
    clean = ""
    idx = 0
    # Search for links in a sentence and replace them with their anchor tezt
    for m in link_re.finditer(sent):
        href, mention = m.groups()
        cui = normalize_title(href, mapping)
        if not cui:
            continue
        clean += sent[idx:m.start()] + mention
        start = len(clean) - len(mention)
        annotations.append((mention, cui, start, start + len(mention)))
        idx = m.end()
    clean += sent[idx:]

    if annotations and "<" not in clean:
        return clean, annotations
    return None


mapping = build_title_map("2_generate_corpus/wikidata_nl.jsonl")
samples = []
rows = []
uid = 0

for root, _, files in os.walk("2_generate_corpus/wikiextractor/outnlcat4"):
    for fn in files:
        with open(os.path.join(root, fn), encoding="utf-8") as f:
            for line in f:
                text = json.loads(line)["text"]

                matches = link_re.findall(text)

                if not any(normalize_title(m[0], mapping) for m in matches):
                    continue

                doc = nlp(text)

                for sent in doc.sents:
                    parsed = parse_sentence(sent.text, mapping)
                    if not parsed:
                        continue

                    sentence, anns = parsed
                    samples.append({
                        "sentence": sentence,
                        "annotations": [
                            {"mention": m, "CUI": c, "start": s, "end": e}
                            for m, c, s, e in anns
                        ]
                    })

                    for m, c, s, e in anns:
                        rows.append({
                            "id": uid,
                            "mention": m,
                            "cui": c,
                            "start_index": s,
                            "end_index": e,
                            "sentence": sentence
                        })
                        uid += 1

pd.DataFrame(rows).to_csv("2_generate_corpus/walvis_nl_cat4.csv", index=False)

print(f"Saved {len(rows)} mentions")
