# File to convert model to REST API and deploy it on local server using Flask

from flask import Flask, request
import pandas as pd # To convert input lists to dataframes
from pii_column_classification import classify

app = Flask(__name__) # Create Flask app instance when main function is called

@app.route('/display_classification', methods = ['POST']) # Action on routing to 'display_classification' subpath of API URL
def display_classification():
    # To load parameters from json body of POST request
    content = request.json
    tn_json = content["Table Names"]
    tc_json = content["Table Columns"]
    
    # To convert input lists to dataframes
    tables = pd.DataFrame(list(zip(tn_json, tc_json)), columns = ['Table Name', 'Table Column'])
    df = pd.read_excel('PII Term Glossary.xlsx') # To read PII terms from glossary file in source code directory
    PII_Terms = list(df['Alias Term'])
    pii_terms = pd.DataFrame(PII_Terms, columns = ['PII Term'])
    
    results = classify(tables, pii_terms) # Calling main classify function

    return results.to_json(orient = 'records') # Return results as json in response

if __name__ == '__main__':
	app.run(debug = True)
