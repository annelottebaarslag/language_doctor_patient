# Train NER model
In this part of the code we train the model which will extract the medical entities from the text. The resulting model has a high recall but a low precision.
## Create NER dataset
Use the notebook `create_NER_dataset.ipynb` for creating the NER dataset which is used for training the model. Our input file is given in this current folder and is called `mm_dut_no_nan.csv`. We also provide the output file called `medmentions_dutch.csv`. This file can be used to reproduce our research. In future research it is recommended to search or create a better Dutch NER dataset.
## Train the model
Use the notebook  `train_NER.ipynb` for training 