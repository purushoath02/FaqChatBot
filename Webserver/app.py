from flask import Flask, redirect, url_for, request, render_template,jsonify
import requests
import json
import re
 
app =Flask(__name__, template_folder= 'templates')
context_set = ""

#Funtion to comuniacate with bot 
def Botsend(s): 
    #val = str(request.args.get('text'))
    data =json.dumps({"sender": "Rasa","message": s})
    headers ={'Content-type': 'application/json', 'Accept': 'text/plain'}
    res =requests.post('http://localhost:5005/webhooks/rest/webhook', data= data, headers=headers)
    res =res.json()
    val = res[0]['text']
    return val

@app.route('/')
def index():
    return render_template('tempindex.html')

@app.route('/process', methods=['POST'])
def process():
    input_text = request.json['input']

    # Perform processing with ChatGPT model
    # Replace the following line with your ChatGPT code
    response = Botsend(input_text)

    

    # Check if the response is an image URL based on a regular expression pattern
    image_pattern = r'(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)'
    if re.match(image_pattern, response):
        response_type = 'image'
        print("Response is image")
    else:
        response_type = 'text'
        print("Response is text")

    #return jsonify(type=response_type, response=response+"::"+response_type)
    return jsonify(type=response_type, response=response)

if __name__ == '__main__':
    app.run()



if __name__ == '__main__':
  app.run(debug=True)