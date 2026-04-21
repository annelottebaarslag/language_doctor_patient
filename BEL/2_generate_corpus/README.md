# Generate corpus
In this part of the code we create a WALVIS corpus.

The following two subtexts are based on [this github repository](https://github.com/umcu/dutch-medical-wikipedia?tab=readme-ov-file).
## Collect the Wiki dump
For collecting the Dutch Wikipedia data, go to [the Dutch Wiki dump](https://dumps.wikimedia.org/nlwiki/) and press on `latest/`. Download the file called `nlwiki-latest-pages-articles.xml.bz2`. For my project I used the dump from 01 October 2025. Move the zip file to `2_generate_corpus`. 
For collecting the English wikipedia data, go to [the English Wiki dump](https://dumps.wikimedia.org/enwiki/) and press on `latest/`. For speed, it is recommended to download `enwiki-latest-pages-articles-multistream.xml.bz2` and `enwiki-latest-pages-articles-multistream-index.txt.bz2`.

## Creating a text file with the medical categories
I provided my .txt file from 13 October 2025 that includes the names of the Wikipedia pages concerning Geneeskunde, called `geneeskunde_aandoening_fysiologie_depth_4.txt`. If you recreate this code later, consider creating your own .txt file, because pages get renamed, added and deleted. You can do so using the following steps:
- Go to https://petscan.wmflabs.org
- Select language nl
- Select depth 4
- Type in the Categories box:
Geneeskunde
Fysiologie
Aandoening
- Select the Page Properties tab, make sure only the category box is checked.
- Select the Output tab and select "Plain text".
- Press "Do it!". 
- Paste the resulting text in a file called `geneeskunde_aandoening_fysiologie_depth_4.txt`, delete all "Categorie:" and move the file into `2_generate_corpus`. 
For creating an English category file, select language "en" instead of "nl" and type the categories in English (Medicine, Medical Condition, Physiology).

## Format the wikipedia files
For reformatting the wiki dump, we use the [wikiextractor](https://github.com/sandertan/wikiextractor/). This appeared not to work with my current python version, so I did it with python 3.8 instead. Do the following commands inside the `2_generate_corpus` directory.
```bash
# Create a new Python 3.8 virtual environment and activate
py -3.8 -m venv venv38
source venv38/Scripts/activate

git clone -b stable_dutch --single-branch https://github.com/sandertan/wikiextractor/
```
In `WikiExtractor.py`, search for the part 
```python
 if options.toHTML:
    text = html.escape(text)
```
and comment it out. This way, the links aren't lost. 
Next, execute this code in a bash terminal:

```bash
cd wikiextractor
python -m WikiExtractor ../nlwiki-latest-pages-articles.xml.bz2 \
    --filter_category ../geneeskunde_aandoening_fysiologie_depth_4.txt \
    -o outnl --json --html
```

If you get an error about the encoding, search in wikiextractor.py and search for 
```python
with open(filter_category) as f: 
```
and replace it by:
```python
with open(filter_category, encoding="utf-8") as f:
```

The result will be a folder named `out` in your `wikiextractor` folder, containing one or multiple folders called `AX` which contains multiple `wikiXX` files. 

For doing the same steps for English, you have to change one line in the github repository. Search for
```python
catRE = re.compile(r'\[\[Categorie:([^\|]+).*\]\].*')
```
and replace it by:
```python
catRE = re.compile(r'\[\[Category:([^\|]+).*\]\].*')
```
Also change the categories file by the English categories file and change the output folder from `outnl` to `outnl` so your Dutch folder doesn't get overwritten.

## Retrieving wikipedia entries
For running the SPARQL query, run `retrieve_query.py`. This part of the code is based on [this part of the repository of Hartendorp et al.](https://github.com/fonshartendorp/dutch_biomedical_entity_linking/blob/main/2_generate_corpus/generate_corpus.py). You can add or delete semantic categories in the excluded list. For retrieving the English query results instead of the Dutch, change the domain variable in `fetch_candidates` from `nl.wikipedia.org` to `en.wikipedia.org`. The resulting jsonl file consists of the results in the format:
    {
      "sentence": "<Sentence>",
      "annotations": [
        {
          "mention": "<mention>",
          "CUI": "<cui>",
          "start": <start index>,
          "end": <end index>
        }
      ]
    },

## Generate Walvis corpus
For generating the Walvis corpus, run `generate_corpus.py`. This will create a csv file with columns id,mention,cui,start_index,end_index,sentence. Walvis* is created later in the `generate_positive_pairs.ipynb` notebook in the folder `4_fine-tuning`. 



