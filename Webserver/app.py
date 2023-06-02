from flask import Flask, redirect, url_for, request, render_template, jsonify
import requests
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ChatLog.db'
db = SQLAlchemy(app)

class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(255))
    bot_response = db.Column(db.String(255))
    
    def __init__(self,user_input,bot_response): 
        self.user_input
        self.bot_response

# Function to communicate with the bot
def send(s):
    data = json.dumps({"sender": "Rasa", "message": s})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data, headers=headers)
    res = res.json()
    if not res:
        val = "Sorry, I don't have a response for this question"
    else:
        val = res[0]['text']
    return val

@app.route('/')
def index():
    return render_template('tempindex.html')

@app.route('/process', methods=['POST','GET'])
def process():
    
    input_text = request.json['input']
    response = send(input_text)
    # Save the conversation in the database
    chat_log = ChatLog(user_input=input_text, bot_response=response)
    db.session.add(chat_log)
    db.session.commit()
    return jsonify(type='text', response=response)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
    #app.run(debug=True)
