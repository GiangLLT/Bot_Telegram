import requests

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

# Thay thế bằng API token và chat ID của bạn
telegram_token = '5353149254:AAH8w0Ifop-MALOCNDK6JtGbtwcREcIAUSI'
chat_id = '-4272801743'

# Nội dung tin nhắn
message = "Hello from Python!"

# Gửi tin nhắn
response = send_telegram_message(telegram_token, chat_id, message)
print(response)
