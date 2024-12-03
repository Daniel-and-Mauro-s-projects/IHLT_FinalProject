# [Dani]:
I think the pipeline should look like this: 
- Preprocessing
  - Tokenization, lemmatization
  - Stopwords filtering?
  - If they differ in very few characters in total, ignore everything and assign a max score. 
- Feature generation
  - Every feature should be in itself a similarity measure between the sentences
  - A lot of features are already in this form, but we can use other information (for example length of sentences), which we should convert to a similarity measure on the same scale (maybe [0, 1]). 
- XGBoost on the features to the similarity score
  - Question: does this also select features? We could do something like a Lasso regression or PCA to use only the relevant features
  - The loss function should be the pearson correlation

## Features: 
1. Length (of course in [0, 1]) (characters or tokens? both maybe) - Dani
   1. Characters 
   2. Tokens
2. Set of tokens - Dani
   1. Different kind of set similarities here too
3. Set of synsets - Mauro
   1. Wu-Palmer
   2. Path
   3. Leacock
   4. Lin
4. Multiset of POS tags - Dani
5. N-grams - Mauro

# MAURO: Possible approach:
Since I'm familiar with **XGBoost**, and I've found would results using it in the past, I would do 
- Pick objective data from the sentences 
  - difference in length
  - difference in words
  - difference in punctuation symbols
  - etc.
- Pick all of the simmilarity metrics we've seen
  - for synsets
    - wu-palmer
    - path-simmilarity
    - Leacock-Chodorow
    - Lin
  - for words, tokens, lemmas (both filtering and without filtering)
    - jaccard 
  - Alternatively look into Noun Phrases and all of this (but it will not be as useful I think)
  - N-gramms
  
  - Things I've seen perform well in SEM EVAL:
    - Distributional thesaurus (I think it is basically synsets)
    - Monolingual Corpora (maybe use this two with Lin Similarity jsut as we did with the Brown Corpus) (We should use Coruña Corpus because I'm from A Coruña) (see https://en.wikipedia.org/wiki/List_of_text_corpora)
    - Multilingual Corpora
    - Wikipedia (I think this is just another corpus)
    - WordNet
    - Distributional similarity
    - KB Similarity
    - POS tagger
    - SMT (Statistical Machine Translation)
    - String Similarity 
      - We could use sequence matcher: gives a ratio of similarity between sentences, recognizes longest string in common ...
    - Stop Words: whether we filter or not