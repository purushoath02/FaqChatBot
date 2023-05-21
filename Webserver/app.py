# from flask import Flask, render_template, request, jsonify
# from rasa.core.agent import Agent

# app = Flask(__name__)

# # Load the trained Rasa model
# model_path = "/home/edr/Kryos/FaqChatbot/ChatBot/models/20230522-022209-cold-hook.tar.gz"
# agent = Agent.load(model_path)

# # async def async_function():
# #     # Your asynchronous code here
# #     await asyncio.sleep(1)
# #     return "Hello from async function!"

# @app.route("/")
# def index():
    
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# async def chat():
#     # Get user message from the request
#     user_message = request.json["message"]

#     # Process user message using the Rasa agent
#     response = agent.handle_text(user_message)
#     #result = await async_function()
#     # Extract the chatbot's response
#     bot_response = response[0]["text"]
#     #print(bot_response)
#     # Return the response to the user
#     return jsonify({"response": bot_response})

# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, redirect, url_for, request, render_template
import requests
import json
 
app =Flask(__name__, template_folder= 'templates')
context_set = ""
 
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':
        val = str(request.args.get('text'))
        data =json.dumps({"sender": "Rasa","message": val})
        headers ={'Content-type': 'application/json', 'Accept': 'text/plain'}
        res =requests.post('http://localhost:5005/webhooks/rest/webhook', data= data, headers=headers)
        res =res.json()
        val = res[0]['text']
        return render_template('tempindex.html', val=val)
    
if __name__ == '__main__':
  app.run(debug=True)