import os, random, pysbd

segmenter = pysbd.Segmenter(language="nl", clean=True)
## Use line below only for evaluation
# val_sentences = segmenter.segment(open("Apply BEL/random_100.txt", "r", encoding='utf-8').read())

random_file = open("Apply BEL/random_100_eval.txt", "w", encoding='utf-8')
for _ in range(100):
    folder = random.choice(os.listdir("Apply BEL/TextData"))
    file = random.choice(os.listdir(f"Apply BEL/TextData/{folder}"))
    fp = os.path.join("Apply BEL/TextData",folder, file)

    with open(fp, encoding="utf-8") as f:
        raw_text = f.read()

    sentences = segmenter.segment(raw_text)
    # Validation
    sentences_long = [s for s in sentences if len(s.split()) > 5]
    ## Evaluation
    # sentences_long = [s for s in sentences if len(s.split()) > 5 and s not in val_sentences]

    random_file.write(f"{random.choice(sentences_long)}\n")

random_file.close()