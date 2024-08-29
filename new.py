import requests

def send_telegram_message(token, username, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': f'@{username}',  # Sử dụng username với định dạng @username
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

# Thay thế bằng API token của bot và username của người nhận
telegram_token = '5353149254:AAH8w0Ifop-MALOCNDK6JtGbtwcREcIAUSI'
username = 'USERNAME_OF_RECIPIENT'  # Không cần @ ở đầu, chỉ username

# Nội dung tin nhắn
message = "Hello from Python using username!"

# Gửi tin nhắn
response = send_telegram_message(telegram_token, username, message)
print(response)
