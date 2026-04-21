
import json
import time
from SPARQLWrapper import SPARQLWrapper, JSON
from pathlib import Path
import csv

umls_csv = "1_enhance_UMLS/04_ConceptDB/umls-dutch_v1.11_with_drugs_filtered-categories.csv"
batch_size = 1000

# excluded semantic groups from the UMLS
excluded = {
    "T078","T089","T011","T008","T012","T013","T015","T001","T014","T010",
    "T168","T093","T083",
    "T056","T065","T064","T170","T171","T073",
    "T057","T090","T066","T092","T072","T067",
    "T097","T094","T080","T081","T095","T082","T079",
}

# load only medical cuis that are not in the excluded tuis
def load_medical_cuis(umls_csv):
    medical_cuis = set()
    with open(umls_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            types = set(row["type_ids"].split("|"))
            if types.isdisjoint(excluded):
                medical_cuis.add(row["cui"])
    return medical_cuis


# sparql query
def build_query(limit, offset, domain):
    return f"""
    SELECT ?article ?concept ?cui WHERE {{
      ?article schema:isPartOf <https://{domain}/> .
      ?article schema:about ?concept .
      ?concept wdt:P2892 ?cui .
    }}
    LIMIT {limit}
    OFFSET {offset}
    """

# execute sparql query and only keep the non excluded cuis
def fetch_candidates(medical_cuis, output_jsonl, domain):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(200)

    output_path = Path(output_jsonl)
    offset = 0

    with open(output_path, "w", encoding="utf-8") as out:
        while True:
            query = build_query(batch_size, offset, domain)
            sparql.setQuery(query)
            print(f"Fetching OFFSET={offset}")

            try:
                results = sparql.queryAndConvert()["results"]["bindings"]
            except Exception as e:
                print(e)
                time.sleep(10)
                continue

            if not results:
                break

            for result in results:
                cui = result["cui"]["value"]

                # only keep the cuis of the non excluded categories
                if cui not in medical_cuis:
                    continue

                record = {
                    "cui": cui,
                    "concept": result["concept"]["value"],
                    "article": result["article"]["value"],
                }

                out.write(json.dumps(record, ensure_ascii=False) + "\n")

            offset += batch_size
            time.sleep(3)

    print("Finished")


cuis = load_medical_cuis(umls_csv)
fetch_candidates(cuis, "2_generate_corpus/wikidata_nl.jsonl", "nl.wikipedia.org")
