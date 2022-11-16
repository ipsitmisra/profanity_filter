#Packages needed to be installed
#!pip install presidio_analyzer
#!python -m spacy download en_core_web_lg
import spacy
nlp = spacy.load('en_core_web_lg')

#Need to import in order to avoid Spacy version errors
import logging
logger = logging.getLogger("spacy")
logger.setLevel(logging.ERROR)

# Call analyzer to get results
from presidio_analyzer import AnalyzerEngine

# Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers
analyzer = AnalyzerEngine()

# Function to calculate Confidence score
def fetch_cs(inp):

  inp = str(inp[0])
  inp = list(inp.split(" "))
  #print(inp)
  
  return inp[-1]

#Function returns 
#1. All Column Names
#2. Sensitive Column Names
#3. Confidence Score of each column
# Parameter passed : json input (dictionary)
def return_pii_data(content):    
  #List created to store confidence scores of respective columns  
  conf_score = []    
  #list created to store Sensitive column names
  PII_Column_names = []

  #Loop through the keys(here, the column names) in content
  for i in content:
    count = 0 # count variable to keep check number of sensitive data found in the column till i'th traversal
    max_cs = 0 #max_cs variable to store highest confidence value against the entires in the column. 
    for x in content[i]:   
      text_new = str(x) + " " + str(i) #String concatenation to make structured data -> unstructured data
      result =  analyzer.analyze(text= text_new, language='en') # call of analyzer function and stired in result.
      if len(result) >= 1:  
        cs = float(fetch_cs(result))  #confidence score calculated for data entry 
        max_cs = max(max_cs, cs)  #max of the score is stored
        count+=1
      if count == 2: #Condition for classifying column as sensitive after two valid data entries
        PII_Column_names.append(i)
        conf_score.append(str(i) + ":" + str(max_cs))
        break      


  
  total_col = []
  for i in content.keys():
    total_col.append(i) 
  

  return_dict = {}
  return_dict['All Columns '] = total_col
  return_dict['Sensitive Columns '] = PII_Column_names
  return_dict['Confidence Scores'] = conf_score
    

  return(return_dict)

    