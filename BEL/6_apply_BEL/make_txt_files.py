import os
import pandas as pd

new_folder = "Apply BEL/TextData/ABEL_text2"
os.makedirs(new_folder, exist_ok=True)

folder = "Apply BEL/Abel_level"

for file in os.listdir(folder):
    path = os.path.join(folder, file)
    name, _ = os.path.splitext(file)   
    df = pd.read_csv(path)
    output_path = os.path.join(new_folder, f"{name}.txt")
    df.to_csv(output_path, sep="\t", header=False, index=False)
