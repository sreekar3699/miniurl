import http.client
import json

def lambda_handler(event, context):
    print(event)
    try:
        body = json.loads(event['body'])
        print(body)
        
        message_part = body['message'].get('text')
        print("Message part : {}".format(message_part))
        
        data = {'url': message_part}
        
        # Making a POST request using http.client
        conn = http.client.HTTPSConnection("cleanuri.com")
        payload = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        conn.request("POST", "/api/v1/shorten", payload, headers)
        
        res = conn.getresponse()
        data = res.read()
        short_url = json.loads(data.decode("utf-8"))['result_url']
        print("The short url is : {}".format(short_url))
        
        chat_id = body['message']['chat']['id']
        send_telegram_message(chat_id,short_url)
    except Exception as e:
        print(e)
        return {"statusCode": 200}
        


def send_telegram_message(chat_id, text):
    
    telegram_bot_token = "7028831379:AAGBX42wM16nM9Q-LFRoYwmhu0L5gq3q7Ug"
    host = "api.telegram.org"
    path = f"/bot{telegram_bot_token}/sendMessage"

    connection = http.client.HTTPSConnection(host)
    
    headers = {"Content-type": "application/json"}
    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    connection.request("POST", path, body=json.dumps(payload), headers=headers)
    response = connection.getresponse()

    # Read and print the response
    response_data = response.read().decode("utf-8")
    print(response_data)

    connection.close()
    return response_data
