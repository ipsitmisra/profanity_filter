# File to compute correlation matrix and perform similarity based operations

import tensorflow as tf
import numpy as np # To perform all array-based operations
# import seaborn as sns # To generate heatmap for correlation matrix (optional)

def compute_similarity(columns, column_embeddings, terms, term_embeddings, tables):
  corr = np.inner(column_embeddings, term_embeddings) # To compute correlation matrix between every column and pii term pair
  corr = tf.clip_by_value(corr, 0.0, 1.0) # To clip every correlation value within 0-1 range
  corr = corr.numpy()

  # print(corr)
  
  # To display correlation matrix in form of a heatmap
  ''' sns.set(font_scale = 1.2)
  graph = sns.heatmap(
      corr.transpose(),
      xticklabels = terms,
      yticklabels = columns,
      vmin = 0,
      vmax = 1,
      cmap = "YlOrRd")
  graph.set_xticklabels(terms, rotation = 90)
  graph.set_title("Semantic Word Similarity")
  fig = graph.get_figure()  
  fig.savefig("heatmap.png", figsize = (16,5)) '''

  # Lists To store the final mappings for all the column names 
  global Mapped_Table_Columns
  global Mapped_Table_Names
  global Mapped_PII_Terms
  global Mapped_Similarities
  global Similarity_Values
  
  Mapped_Table_Columns = []
  Mapped_Table_Names = []
  Mapped_PII_Terms = []
  Mapped_Similarities = []
  Similarity_Values = []

  print()

  for i in range(corr.shape[0]): # To iterate through correlation values for each column name
    # Lists to store mapping for each column name
    Mapped_Columns = []
    Mapped_Tables = []
    Mapped_Terms = []
    Similarities = []
    Mapped_Similarity_Values = []

    if(max(corr[i]) >= 0.5): # To store mappings only if highest semantic similarity is atleast 50% (i.e. it is a sensitive column)
        max_similarity_pii_term = np.argmax(corr[i]) # To determine index of PII term with highest similarity
    
	# To store mapping of column with highest similarity value
        Mapped_Columns.append(columns[i])
        Mapped_Tables.append(tables[i])
        Mapped_Terms.append(terms[max_similarity_pii_term])
        Similarities.append(round(max(corr[i]) * 100, 2))
        Mapped_Similarity_Values.append(str(round(max(corr[i]) * 100, 2)) + "%") # Rounding similarity value to 2 places after decimal point

	# To iterate through correlation values with every other column name
        ''' for j in range(len(corr[i])):
          if((corr[i][j] >= 0.9 or columns[j] == Mapped_Columns[0]) and j != max_similarity_column): # To store mapping with every other column only if semantic similarity is atleast 90%
            Mapped_Terms.append(terms[i])
            Mapped_Columns.append(columns[j])
            Mapped_Dashboards.append(dashboards[j])
            Mapped_Similarity_Values.append(str(round(corr[i][j] * 100, 2)) + "%") '''

    # If highest similarity is less than 50%, store no mapping for the column name (i.e. it is not a sensitive column)
    else:
        Mapped_Columns.append(columns[i])
        Mapped_Tables.append(tables[i])
        Mapped_Terms.append("")
        Mapped_Similarities.append(round(max(corr[i]) * 100, 2))
        Mapped_Similarity_Values.append("")

    # print("The mapping for the business term ", terms[i], "is the column: ", Mapped_Columns[0], "of the dashboard: ", Mapped_Dashboards[0], "with semantic similarity percentage: ", Mapped_Similarity_Values[0], end = "\n\n")

    # To append the mapping for particular business term to the overall final mappings list
    Mapped_Table_Columns.extend(Mapped_Columns)
    Mapped_Table_Names.extend(Mapped_Tables)
    Mapped_PII_Terms.extend(Mapped_Terms)
    Mapped_Similarities.extend(Similarities)
    Similarity_Values.extend(Mapped_Similarity_Values)
