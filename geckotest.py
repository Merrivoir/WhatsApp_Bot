import requests

url = "https://7103.api.greenapi.com/waInstance7103145111/sendMessage/44cb1aca56fb4b02b4466c4c18b31a1583fb88b9b9634ff7b5"

payload = {
"chatId": "77474728450@c.us", 
"message": "Тест сообщения"
}
headers = {
'Content-Type': 'application/json'
}

response = requests.post(url, json=payload, headers=headers)

print(response.text.encode('utf8'))