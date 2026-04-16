# NER and BEL on Dutch consults between doctor and cancer consults
This code exists of 7 folders for the different parts of the pipeline.
- `1_enhance_UMLS` is for creating our enhanced ontology in csv file format with columns cui,name,type_ids,ontologies,name_status.
- `2_generate_corpus` is for creating a WALVIS corpus.
- `3_pretraining` is for 2nd phase pretraining of sapBERT using the enhanced UMLS we created in `1_enhance_UMLS`.
- `4_fine-tuning` is for creating WALVIS*, a filtered version of the corpus we created in `2_generate_corpus` and then using WALVIS* for finetuning the model we pretrained in `3_pretraining`.
- `5_train_NER_model` is for creating a NER dataset and then using that dataset to train MedRoBERTa.nl for NER.
- `6_apply_BEL` is for creating text files from the consults and then validating and evaluating the NER model trained in `5_train_NER_model` and the BEL model finetuned in `4_fine-tuning` before applying them to the consults.
- `7_analyze_results` is for analyzing the results which were created in `6_apply_BEL`. The results of the code in this folder is shown in the thesis.

