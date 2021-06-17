import requests

name = input('Введите имя==>>')
while True:
    text = input()
    response = requests.post('http://127.0.0.1:5000/send',
                  json={'name': name, 'text': text}
    )

#print(response.status_code)
#print(type(response.text))
#print(response.text)
