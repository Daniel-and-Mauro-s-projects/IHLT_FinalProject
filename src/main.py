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

import nltk
from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic
nltk.download('wordnet')
nltk.download('wordnet_ic')
ic_brown = wordnet_ic.ic('ic-brown.dat')

import numpy as np
from joblib import Parallel, delayed

sentences_file_path = "../Data/Train/train/STS.input.SMTeuroparl.txt"
gold_standard_file_path = "../Data/Train/train/STS.gs.SMTeuroparl.txt"

sentences: pd.DataFrame = pd.read_csv(sentences_file_path ,sep='\t',header=None)
gs: pd.DataFrame = pd.read_csv(gold_standard_file_path, header=None)
features: pd.DataFrame = pd.DataFrame()

sentences["0_lower"] = sentences[0].apply(lambda x: x.lower())
sentences["1_lower"] = sentences[1].apply(lambda x: x.lower())

sentences["0_nlp"] = sentences["0_lower"].apply(lambda x: nlp(x))
sentences["1_nlp"] = sentences["1_lower"].apply(lambda x: nlp(x))

# Features

## Synset Similarities:
def get_wordnet_pos(category):
    """
    Convert a POS tag from the Spacy tagset to the WordNet tagset.
    """
    if category.startswith('J'):
        return 'a'  # Adjective
    elif category.startswith('V'):
        return 'v'  # Verb
    elif category.startswith('N'):
        return 'n'  # Noun
    elif (category.startswith('R')) and (category != 'RP'):
        # I looked into the RP tag is for particles
        return 'r'  # Adverb
    else:
        return None  # WordNet doesn't handle other POS tags

cache = {}
def get_best_synset_pair(word1, word2, pos, similarity, similarity_type):
    """
    Get the best synset pair for two words.

    This function gets the best synset pair for two words, considering every possible pair of synsets from the two words. The best pair is the one with the highest similarity score.

    Parameters:
    - word1: The first word, represented as a Spacy token.
    - word2: The second word, represented as a Spacy token.
    - pos: A string indicating the part of speech of the words.
    - similarity: A function to calculate the similarity between two synsets.
    - similarity_type: A string indicating the name of the similarity measure.

    Returns:
    - A float representing the similarity score of the best synset pair.
    """
    # Create a cache key (I do this because it is simetric and to save time)
    cache_key = tuple(sorted([word1.text, word2.text]) + [similarity_type]) 
    if cache_key in cache:
        return cache[cache_key]

    synsets_word1 = wordnet.synsets(word1.text, pos=pos)
    synsets_word2 = wordnet.synsets(word2.text, pos=pos)
    max_sim = 0

    for synset1 in synsets_word1:
        for synset2 in synsets_word2:
            sim = similarity(synset1, synset2)
            if sim and sim > max_sim:
                max_sim = sim
    
    cache[cache_key] = max_sim
    # If there is no similarity, we return 0
    return max_sim

def get_sentence_similarities(sentence1, sentence2, similarity_type):
    """
    Calculate the similarity between two sentences using a specified similarity measure.

    For each sentence, the function gets the best similarity value for each word considering every posible pair, using words from the other sentence. Then the mean of this similarities is computed over the sentence and the output is the mean similarity of the two sentences.

    Parameters:
    - sentence1: The first sentence, represented as a list of tokens.
    - sentence2: The second sentence, represented as a list of tokens.
    - similarity_type: A string indicating the type of similarity measure to use. 
        Options include "wu-palmer", "path", "leacock", and "lin".

    Returns:
    - A float representing the average similarity score between the two sentences.
    """
    # TODO: Judge if we want to normalize by the number of words that have a valid POS for WordNet
    similarity_methods = {
        "wu-palmer": lambda s1, s2: s1.wup_similarity(s2),
        "path": lambda s1, s2: s1.path_similarity(s2),
        "leacock": lambda s1, s2: s1.lch_similarity(s2),
        "lin": lambda s1, s2: s1.lin_similarity(s2, ic_brown)
    }
    similarity1 = 0
    den = 0 # We will normalize by the number of words that have a valid POS for WordNet
    for token1 in sentence1:
        similarities = np.array([])
        pos1 = get_wordnet_pos(token1.tag_)
        if not pos1:
            continue
        den +=1
        for token2 in sentence2:
            pos2 = get_wordnet_pos(token2.tag_)
            if (not pos2) or (pos1 != pos2):
                continue
            similarities = np.append(similarities,get_best_synset_pair(token1, token2, pos1, similarity_methods[similarity_type], similarity_type))
        if similarities.size > 0:
            similarity1 += np.max(similarities)
    # We average the similarity (even if they don't get a similarity)
    similarity1 = similarity1 / den

    similarity2 = 0
    den = 0 # We will normalize by the number of words that have a valid POS for WordNet
    for token2 in sentence2:
        similarities = np.array([])
        pos2 = get_wordnet_pos(token2.tag_)
        if not pos2:
            continue
        den +=1
        for token1 in sentence1:
            pos1 = get_wordnet_pos(token1.tag_)
            if (not pos1) or (pos1 != pos2):
                continue
            similarities = np.append(similarities, get_best_synset_pair(token1, token2, pos2, similarity_methods[similarity_type], similarity_type))
        if similarities.size > 0:
            similarity2 += np.max(similarities)
    # We average the similarity (even if they don't get a similarity)
    similarity2 = similarity2 / den
    print(f"For sentence 2| Words with pos tag: {den}, size of sentence: {len(sentence2)}")
    return np.mean(np.array([similarity1, similarity2]))

# ### Wu-Palmer Similarity
# def compute_wu_palmer(row):
#     return get_sentence_similarities(row["0_nlp"], row["1_nlp"], "wu-palmer")

# features["wu-palmer"] = Parallel(n_jobs=-1)(delayed(compute_wu_palmer)(row) for _, row in sentences.iterrows())
features["wu-palmer"] = sentences.apply(lambda row: get_sentence_similarities(row["0_nlp"], row["1_nlp"], "wu-palmer"), axis=1)




# Display the DataFrame
print(features[0:50])



