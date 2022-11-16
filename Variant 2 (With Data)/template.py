# File to convert model to REST API and deploy it on local server using Flask
import json
from flask import Flask, request
from pii_scan import return_pii_data

app = Flask(__name__) # Create Flask app instance when main function is called

@app.route('/display_pii', methods = ['POST']) # On routing to 'display_mapping' subpath of API URL
def display_pii():
    # To load parameters from json body of POST request
    content = request.json   
   
    results = return_pii_data(content) # Calling main mapping function

    #return results.to_json(orient = 'records')
    
    return json.dumps({'results': results})

if __name__ == '__main__':
	app.run(debug = True)
