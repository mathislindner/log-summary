import json

from model import ChatModel

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

# Enable cors requests
CORS(app) 

#Initiate model
clf = ChatModel()

@app.route('/')
def index():
    """Check if api is working."""
    return json.dumps({'status': 'OK'})

@app.route('/query', methods=['POST'])
def query():
    """Endpoint for receiving bot response"""
    query = request.json
    input_data = query['userQuery']
    bot_answer = clf.get_reply(input_data)
    return json.dumps(bot_answer)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000
    )

#prompt example
"""
curl -X POST localhost/query -H 'Content-Type: application/json' -d '{"userQuery":"Human: oh what a lovely day to be alive, what can you tell me about being alive? \n AI: "}'
"""