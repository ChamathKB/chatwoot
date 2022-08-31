import requests

rasa_url = 'http://localhost:5005/webhooks/shoutout_telegram/webhook'
chatwoot_url = 'http://localhost:3000'
chatwoot_bot_token = 'RHd4tJf2daEGbR3BqKVPtSQq'


def send_to_bot(sender, message, messageItem):
    data = {
        'sender': sender,
        'message': message,
        'messageItem': messageItem
    }
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    r = requests.post(url=rasa_url,
                      json=data, headers=headers)
    print("bot: ", r.text)
    return r.json()[0]['text']


def send_to_chatwoot(account, conversation, message):
    data = {
        'content': message
    }
    url = f'{chatwoot_url}/api/v1/accounts/{account}/conversations/{conversation}/messages'
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "api_access_token": f"{chatwoot_bot_token}"}

    r = requests.post(url,
                      json=data, headers=headers)
    print("chatwoot: ", r.text)
    return r.json()


from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=['POST'])
def rasa():
    data = request.get_json()
    print(data)
    message_type = data['message_type']
    message = data['content']
    conversation = data['conversation']['id']
    contact = data['sender']['id']
    account = data['account']['id']
    messageItem = data['conversation']['messages'][0]

    if(message_type == "incoming"):
        bot_response = send_to_bot(contact, message, messageItem)
        create_message = send_to_chatwoot(
            account, conversation, bot_response)
    return create_message

if __name__ == '__main__':
    app.run(debug=1, port=8000)
    # print(send_to_chatwoot(2,12,'3'))
