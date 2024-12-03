## ONLY TO EXTRACT THE FILES

# import tarfile

# train_file_path = "../Data/train.tgz"
# extraction_path = "../Data/Train/"
# # Open the .tgz file
# with tarfile.open(train_file_path, "r:gz") as tar:
#     # Extract all contents to the specified directory
#     tar.extractall(path=extraction_path)
#     print(f"Extracted all files to '{extraction_path}'")

import pandas as pd
import spacy
nlp = spacy.load("en_core_web_sm")

sentences_file_path = "../Data/Train/train/STS.input.SMTeuroparl.txt"
gold_standard_file_path = "../Data/Train/train/STS.gs.SMTeuroparl.txt"

sentences: pd.DataFrame = pd.read_csv(sentences_file_path ,sep='\t',header=None)
gs: pd.DataFrame = pd.read_csv(gold_standard_file_path, header=None)
features: pd.DataFrame = pd.DataFrame()

sentences["0_lower"] = sentences[0].apply(lambda x: x.lower())
sentences["1_lower"] = sentences[1].apply(lambda x: x.lower())

sentences["0_nlp"] = sentences["0_lower"].apply(lambda x: nlp(x))
sentences["1_nlp"] = sentences["1_lower"].apply(lambda x: nlp(x))

# Display the DataFrame
print(sentences["0_nlp"])



