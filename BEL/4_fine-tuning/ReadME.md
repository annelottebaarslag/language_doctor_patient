# Finetuning
In this part we finetune the model using the WALVIS corpus that we created in `2_generate_corpus`. The creating of the positive pairs and finetuning are mainly copied from [the finetuning part of the repository of Hartendorp et al](https://github.com/fonshartendorp/dutch_biomedical_entity_linking/tree/main/4_fine-tuning) and the creating of the index of the [evaluate part of the repository](https://github.com/fonshartendorp/dutch_biomedical_entity_linking/blob/main/5_evaluate/build_index.ipynb).

## Translating the English pairs
The notebook `translate_pairs.ipynb` can be used to create translated pairs from the English walvis corpus. Move the translated file into this folder, `4_fine-tuning`.

## Creating the pairs for finetuning
The notebook `generate_positive_pairs.ipynb` is used for creating the pairs for finetuning from the WALVIS corpus. The first part of the notebook creates the positive pair file from the Dutch WALVIS corpus. The second part of the notebook cleans up the translated English pairs and combines the Dutch and translated pair files into one file, which is used in `finetune.ipynb`.

## Finetuning
The notebook `finetune.ipynb` is used for finetuning the model which was pretrained in `3_2nd-phase-pretraining`. 
