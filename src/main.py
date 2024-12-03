# import tarfile

# train_file_path = "../Data/train.tgz"
# extraction_path = "../Data/Train/"
# # Open the .tgz file
# with tarfile.open(train_file_path, "r:gz") as tar:
#     # Extract all contents to the specified directory
#     tar.extractall(path=extraction_path)
#     print(f"Extracted all files to '{extraction_path}'")

import pandas as pd

# Path to the text file
file_path = "../Data/Train/train/STS.input.SMTeuroparl.txt"
gold_standard_file_path = "../Data/Train/train/STS.gs.SMTeuroparl.txt"

# Read the text file and split into a DataFrame
df = pd.read_csv(file_path ,sep='\t',header=None)

df['gs'] = pd.read_csv(gold_standard_file_path, header=None)

# Display the DataFrame
print(df.head)



