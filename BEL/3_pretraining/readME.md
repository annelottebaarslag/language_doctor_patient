# 2nd phase pretraining #
In this part we perform 2nd phase pretraining of sapBERT.

## Generating positive pairs ##
First, use the notebook ``generate_positive_pairs.ipynb`` to generate the file for the pretraining using the enhanced UMLS which was created in ``1_enhance_UMLS``. In order to do so we need sapBERT. SapBERT can be downloaded from the GitHub repository https://github.com/cambridgeltl/sapbert. Next, unzip the folder and move it into this folder, ``3_2nd_phase-pretrain_sapBERT``. 

## Pretraining ##
Once we have the positive pair file and downloaded sapBERT we can use the file for pretraining. Execute the notebook called ``pretrain.ipynb`` in order to do so. It is highly recommended to execute this code on GPU.