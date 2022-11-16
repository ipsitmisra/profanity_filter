import time # To compute runtime of the program

start = time.time() # Time during start of the program

import pandas as pd # To perform basic preprocessing and convert final output to dataframe 
import embed_and_compute # File to embed column names and PII terms
import compute_similarity # File to compute correlation matrix and perform similarity based operations

# Main calling function for the API
def classify(tables, pii_terms):

  # Basic preprocessing to remove duplicates and NaN values from input dataframe
  tables.drop_duplicates(keep = 'first', inplace = True)
  tables.fillna("", inplace = True)

  Table_Names = list(tables['Table Name'])
  Table_Columns = list(tables['Table Column'])

  PII_Terms = list(pii_terms['PII Term'])

  embed_and_compute.embed_and_compute(Table_Names, Table_Columns, PII_Terms) # Calling of function to embed column name and PII term strings

  column_sensitivities = ["Sensitive" if similarity >= 90.00 else "Non-sensitive" for similarity in compute_similarity.Mapped_Similarities] # To classify column names as sensitive or non-sensitive based on mapped PII term
  
  dict1 = {'Table Name' : compute_similarity.Mapped_Table_Names, 'Table Column': compute_similarity.Mapped_Table_Columns, 'Sensitivity' : column_sensitivities, 
           'Mapped PII Type': compute_similarity.Mapped_PII_Terms, 'Sensitivity Percentage' : compute_similarity.Similarity_Values} # Mappings in form of a dictionary
  df = pd.DataFrame(dict1)

  end = time.time() # Time during end of the program
  print(f"Runtime of the program is {end - start} seconds.")

  return df # Returns mapping dataframe to API
