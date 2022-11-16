# File to embed column names and PII terms

import tensorflow_hub as hub # To load the 'Universal Sentence Encoder' model
import tensorflow as tf # To normalize embeddings
import re # To determine regular expression patterns
from compute_similarity import compute_similarity

# Function to embed column names and PII terms
def embed_and_compute(names_, columns_, terms_):
  columns = columns_.copy()
  terms = terms_.copy()

  # Basic preprocessing to remove all special characters and spaces in column names
  for i in range(len(columns)):
    columns[i] = re.sub('[^a-zA-Z0-9\n\.]', '', columns[i])

  embed = hub.load("universal-sentence-encoder-large_5") # To load the pretrained Universal Sentence Encoder model

  #To encode column names and PII terms to higher-dimensional (size- 1 x 512) numeric vectors
  column_embeddings_ = tf.nn.l2_normalize(embed(tf.constant(columns)), axis = 1)
  term_embeddings_ = tf.nn.l2_normalize(embed(tf.constant(terms)), axis = 1)

  # print(term_embeddings_[0])
  
  ''' cosine_similarities = tf.reduce_sum(tf.multiply(term_embeddings, column_embeddings), axis = 1)
  cosine_similarities = tf.clip_by_value(cosine_similarities, -1.0, 1.0)
  similarity_scores = 1.0 - tf.acos(cosine_similarities) / math.pi
  print(similarity_scores) '''

  compute_similarity(columns_, column_embeddings_, terms_, term_embeddings_, names_) # Calling function to compute correlation matrix and perform similarity based operations
