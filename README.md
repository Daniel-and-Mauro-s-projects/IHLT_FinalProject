## Semantic Textual Similarity Project (SemEval 2012)

**Authors:** Dániel MÁCSAI, Mauro VÁZQUEZ CHAS
**UPC - Master in Artificial Intelligence - Introduction to Human Language Technology**
**Final project - 12th December 2024**

The goal of this project is to predict the semantic similarity label for pairs of sentences, as part of the SemEval 2012 task.

### Semantic Similarity Labels

For paraphrase detection, a similarity value is assigned to each sentence pair. The following table defines the meaning of these labels:

| Label | Description                                                    |
|-------|----------------------------------------------------------------|
| 5     | Completely equivalent, meaning the same thing.                   |
| 4     | Mostly equivalent, with minor unimportant differences.          |
| 3     | Roughly equivalent, with some important differences or missing information. |
| 2     | Not equivalent, but share some details.                          |
| 1     | Not equivalent, but on the same topic.                           |
| 0     | On different topics.                                            |

### Features
* Basic features: token and character ratios, Levenshtein distance
* Jaccard similarity: on tokens, lemmas, and synsets
* WordNet similarities: Wu-Palmer, Path, Leacock
* N-gram features: word and character n-grams (Jaccard and vector-based similarities)
* SentiWordNet: sentiment difference between Lesk synsets

### Evaluation
In this task, Pearson correlation is used for comparison purposes to evaluate the performance of the model.

### Contributing
Feel free to contribute by reporting issues, suggesting improvements, or implementing new features.