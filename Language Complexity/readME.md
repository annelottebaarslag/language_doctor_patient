# Language complexity
This folder contains all files for calculating and analyzing the language complexity of doctor and patient in the consults.
## Make dataset
The file `makedataset.py` is for creating structured files from the consults which can be used for analysis.
## Classifier
The file `classifier.py` is for using a classifier to distinguish between doctor and patient turns. The results correspond to the thesis section "Distinguishing doctor and patient turns with a classifier".
## Complexity analysis
The notebook `complexity_analysis.ipynb` is for:
- Calculating the text metrics (corresponding to thesis section "General language complexity"), the boxplots are created in `complexity_boxplots.py`
- Calculating the total of words and syllables which can be used for the dialogue pace (see next section)
- Calculating the change in language complexity, corresponding to thesis section "Language complexity adaptation".
## Duration
The file `extract_duration.py` is for extracting the duration from IBIS and IBIS colon. In the notebook `complexity_analysis.ipynb` the total words and syllables are calculated, which are used for calculating the pace. The notebook `pace_analysis.ipynb` is for using this duration for calculating the correlation between the duration and the language complexity of the doctor and for determining the average words/turn from doctor and patient. The results correspond to the thesis section "Dialogue pace". 
## Correlation
The notebook `correlation.ipynb` is for calculating the correlation between text metrics and education level (corresponding to thesis section "Correlation text metrics with patient education level") and correlation between FRE score and jargon use (corresponding to thesis section "Correlation language complexity and jargon use").

