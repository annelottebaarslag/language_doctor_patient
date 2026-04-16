This folder is forked from [https://github.com/umcu/dutch-medical-concepts](https://github.com/umcu/dutch-medical-concepts)

# Dutch Medical Concepts
This repository contains instructions and code to create concept tables of Dutch medical names, such as primary names, synonyms, abbreviations, and common misspellings. By basing a concept table on UMLS, which includes MeSH, MedDRA, ICD-10 and ICPC, and adding 
 CT and a few manually added names, a comprehensive set of words commonly used in Dutch medical language is generated. Workflows for creating SNOMED concept tables are also in this repository.

The resulting concept tables can be used in named entity recognition and linking methods, such as MedCAT, to identify entities in Dutch medical text. 

| Ontology | Number of concepts | Number of names | Primary source |
| - | - | - | - |
| Dutch UMLS | 254835 | 574475 | UMLS 2022AB |
| Dutch UMLS with English drug names | 367913 | 754326 | UMLS 2022AB |
| Dutch SNOMED | 230277 | 521118 | SNOMED CT Netherlands Edition September 2022 v1.0 |
| Dutch HPO | 13360 | 29164 | [Dutch HPO translations](https://crowdin.com/project/hpo-translation/nl) |

Data and licenses should be acquired from [UMLS Terminology Services](https://uts.nlm.nih.gov/uts/) and [SNOMED MLDS](https://mlds.ihtsdotools.org/). 

## Table of Contents
- [Folder structure](#folder-structure)
- [Output format](#output-format)
- [Data-flow](#data-flow)
- [Generate UMLS concept table](#generate-umls-concept-table)
	- [1. Obtain license and download complete UMLS](#1-obtain-license-and-download-complete-umls)
	- [2. Decompress and install MetamorphoSys](#2-decompress-and-install-metamorphosys)
	- [3. Select UMLS concepts for Dutch medical language using MetamorphoSys](#3-select-umls-concepts-for-dutch-medical-language-using-metamorphosys)
	- [4. Load all terms in a SQL database](#4-load-all-terms-in-a-sql-database)
	- [5. Create concept table](#5-create-concept-table)
- [Generate SNOMED concept table](#generate-snomed-concept-table)
- [Generate HPO concept table](#generate-hpo-concept-table)
- [Generate MedCAT models](#generate-medcat-models)

## Folder structure
The methods of this repository require a number of input files, which should be downloaded by the user, and intermediate and output files are generated. This repository contains a folder structure that can be used for storing these files. The contents of these folders, except for `05_CustomChanges`, are added not tracked by Git, which makes it easier to replace input files or recreate output files.
```
dutch-medical-concepts
└───01_Download
└───02_ExtractSubset
└───03_SqlDB
└───04_ConceptDB
└───05_CustomChanges
```

## Output format
| cui      | name                     | ontologies           | name_status | type_ids |
|----------|--------------------------|----------------------|-------------|----------|
| C0000001 | kanker                   | ONTOLOGY1\|ONTOLOGY2 | P           | T001     |
| C0000001 | neoplasma maligne        | ONTOLOGY1            | A           | T001     |
| C0000002 | longkanker               | ONTOLOGY1            | P           | T001     |
| C0000003 | kleincellige longkanker  | ONTOLOGY1            | P           | T001     |
| C0000004 | chirurgie                | ONTOLOGY1            | P           | T002     |
| C0000004 | chirurgische verrichting | ONTOLOGY1            | A           | T002     |
| C0000005 | chirurgie                | ONTOLOGY1            | P           | T003     |
| C0000005 | specialisme chirurgie    | ONTOLOGY1            | A           | T003     |

See https://github.com/CogStack/MedCAT/tree/master/examples for a detailed explanation of the columns.

This repository uses mock data in the examples.

## Generate UMLS concept table
### 1. Obtain license and download complete UMLS 
To download UMLS, visit the [NIH National Library of Medicine website](https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html). You'll have to apply for a license before you can download the files on https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html. In the following description I downloaded `Full Release (umls-2025AA-full.zip)` and add it to `01_Download/2025AA-full`. The advantage over `UMLS Metathesaurus Full Subset` is that the Full Release includes MetamorphoSys which makes it possible to create a subset of UMLS prior loading the data in a SQL database. This significantly decreases the required disk space and processing time.

### 2. Decompress and install MetamorphoSys
After decompressing the `*-full.zip` file, decompress `mmsys.zip`. Afterwards, move the files in the new `mmsys` folder one level up, so they are in `2025AA-full`. Next, run MetamorphoSys: for macOS, open `./run_mac.sh`, for Windows open either `./run.bat` or `./run64.bat`, depending on if your system is 32 or 64 bit.

### 3. Select UMLS concepts for Dutch medical language using MetamorphoSys
MetamorphoSys is used to install a subset of UMLS. During the installation process it is possible to select multiple sources, and thereby to craft a specific subset for your use case. In our case, our primary goal is to select the Dutch terms and we add some English sources for concept categories for common used English names in Dutch (such as drug names).

- Select `Install UMLS`.
- Select destination directory `./02_ExtractSubset/2025AA/`
- Keep `Metathesaurus` checked, and uncheck `Semantic Network` and `SPECIALIST Lexicon & Lexical Tools`. Select `OK`.
- Select `New Configuration...`, click `Accept` and click `Ok`. The `Default Subset` does not matter because we are making our own subset in the next step.
- In the `Output Options` tab, select `MySQL 5.6` under `Select database`.
- In the `Source List` tab, Select `Select sources to INCLUDE in subset`. Sort the sources on the language column and at least select the 7 Dutch sources. To select multiple sources, hold the CMD key on macOS or the Ctrl key on Windows. In the popup window that will ask if you also want to include related sources, click `Cancel`. The Dutch sources we included were:

| Source name | Source ID |
|---|---|
| ICD10, Dutch Translation, 200403 | ICD10DUT_200403 |
| ICPC2-ICD10 Thesaurus, Dutch Translation | ICPC2ICD10DUT_200412 |
| ICPC2E Dutch | ICPC2EDUT_200203 |
| ICPC, Dutch Translation, 1993 | ICPCDUT_1993 |
| LOINC Linguistic Variant - Dutch, Netherlands | LNC-NL-NL_273 |
| MedDRA Dutch | MDRDUT25_0 |
| MeSH Dutch | MSHDUT2005 |

More information on the sources can be found at: https://www.nlm.nih.gov/research/umls/sourcereleasedocs/index.html

- For drug names some commonly used synonyms in Dutch langague are missing in these vocabularies. Therefore we also selected the following English sources:
  - `ATC_2022_22_09_06`
  - `DRUGBANK5.0_2022_08_01`
  - `RXNORM_20AA_220906F`.
  - `SNOMEDCT_US_2022_09_01`
  - `HPO2020_10_12`
  - `MTH`
- In the `Suppressibility` tab unsuppress the "Abbreviation in any source vocabulary" (`AB`) concepts from MedDRA.
- On macOS, in the top bar, select `Advanced Suppressibility Options` and check all checkboxes. This makes sure the suppressed terms are excluded from the subset. On Windows this menu is under `Options`. 
- In the top bar, select `Done` and `Begin Subset`. This process takes 5-10 minutes.
- Save the SubSet log for future reference.

### 4. Load all terms in a SQL database
To select only the columns required for the target list of terms, first put all the resulting subset in a SQL DB. Open a bash terminal and then enter the following commands line by line.

```bash
# Create local .env file
cp .env-example .env

# Set local file paths & MySQL root password in .env

# Set MySQL loading config settings 
vim ./02_ExtractSubset/2025AA/META/populate_mysql_db.sh

# Press enter and then i for inserting and then replace the first 4 code lines by these lines (replace the password with your password):
# Also update the password in the docker-compose.yml
MYSQL_HOME=/usr
user=root
password=${MYSQL_ROOT_PASSWORD}
db_name=umls

# Press enter and then :wq for saving the file and closing vim.

# Navigate to the 1_enhance UMLS folder
# Start MySQL container in Docker
docker-compose up -d

# Enter docker container
docker exec -it umls bash

# Execute mysql loading script
cd /src_files/2025AA/META/
bash populate_mysql_db.sh
```

The official documentation for loading UMLS in a MySQL DB can be found at [here](https://www.nlm.nih.gov/research/umls/implementation_resources/scripts/README_RRF_MySQL_Output_Stream.html).


### 5. Create concept table
## Generate SNOMED concept table
To setup the Python environment, install the required Python Packages with PIP:
```bash
pip install -r requirements.txt
```
Unzip the downloaded Snomed folder and put the folder in it in `./01_Download`. The method for generating the SNOMED concept table is in [dutch-snomed_to_concept-table.ipynb](dutch-snomed_to_concept-table.ipynb).

## Generate UMLS concept table
Some source vocabularies contain concept types that are not useful for entity 
linking. Also, Dutch vocabularies in UMLS do not contain many drug names. Use 
[dutch-umls_to_concept-table.ipynb](dutch-umls_to_concept-table.ipynb) to:
  - Download concepts, names and types from the MySQL database
  - Remove irrelevant concepts based on term type in source vocabulary
  - Remove irrelevant concepts based on UMLS type
  - Remove problematic names for Dutch language
  - Add many concepts and synonyms from Dutch SNOMED
  - Add custom names
  - Save the concept table in a format compatible with MedCAT

## Manual changes
We made a couple of manual changes after creating the UMLS csv:
- We added "chemo" to C3665472 (status A)
- We deleted "chemotherapie" from C0013216
- We changed C0000726 the preferred name to "abdomen"
- We changed C0279025 the preferred name to "endocriene therapie"
- We made "trombocyten" the preferred name (P) from C1550664
