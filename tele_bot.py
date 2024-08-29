import requests
import time
import pandas as pd
import os

token = '5353149254:AAH8w0Ifop-MALOCNDK6JtGbtwcREcIAUSI'  # Thay thế bằng token của bạn

# Thay thế bằng API Key của bạn
api_key = '617f4b78-83df-4b39-a9c3-6532ee48a84c'

def get_updates(token, offset=None):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=payload)
    return response.json()

def handle_message(message):
    chat_id = message['chat']['id']
    print(chat_id)
    # chat_id = "-4272801743"
    text = message.get('text')

    if text and text.startswith('/function'):
        try:
            command = text.split(' ', 1)[1]  # Lấy phần sau "/function"       
            if command == 'list':
                # Thực hiện đoạn code Python khi nhận được lệnh /function load_data
                # Ví dụ: Tải dữ liệu từ file hoặc xử lý dữ liệu
                List_1 = "List function process:"
                List_2 = "1/ /function List       - Danh sách function hệ thống hỗ trợ."
                List_3 = "2/ /function Load_data  - Load dữ liệu hệ thống."
                List_4 = "3/ /function Reset_data - Reset dữ liệu hệ thống."

                result = f"{List_1} \n {List_2} \n {List_3} \n {List_4} \n"
                send_message(token, chat_id, result)
            elif command.lower() == 'load_data':
                result = "Data loaded successfully!"
                send_message(token, chat_id, result)
            else:
                send_message(token, chat_id, "Unknown command.")
        except Exception as e:
            send_message(token, chat_id, "Unknown command.")
            pass

def get_cryptocurrency_data(api_key):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',         # Vị trí bắt đầu
        'limit': '10',        # Số lượng đồng tiền cần lấy
        'convert': 'USD'      # Đồng tiền quy đổi
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }
    
    response = requests.get(url, headers=headers, params=parameters)
    return response.json()

def send_document(token, chat_id, file_path):
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    with open(file_path, 'rb') as file:
        response = requests.post(url, data={'chat_id': chat_id}, files={'document': file})
    return response.json()

def convert_data_to_dataframe(data):
    # Lấy danh sách các đồng tiền
    cryptocurrencies = data.get('data', [])
    
    # Tạo danh sách các từ điển để chuyển thành DataFrame
    rows = []
    for crypto in cryptocurrencies:
        row = {
            'Name Coin            ': crypto['name'],
            'Symbol Coin          ': crypto['symbol'],
            'Price Coin (USD)     ': crypto['quote']['USD']['price'],
            # 'Market Cap (USD)': crypto['quote']['USD']['market_cap'],
            # '24h Volume (USD)': crypto['quote']['USD']['volume_24h'],
            # 'Change (24h)': crypto['quote']['USD']['percent_change_24h']
        }
        rows.append(row)
    
    # Chuyển dữ liệu thành DataFrame
    df = pd.DataFrame(rows)
    return df

def save_dataframe_to_csv(df, file_path):
    df.to_csv(file_path, index=False)
    
def dataframe_to_text(df):
    # Chuyển DataFrame thành văn bản với định dạng cột
    output = df.to_string(index=False)  # Không bao gồm chỉ số
    return output

def format_dataframe_as_text1(df):
    # Chuyển DataFrame thành văn bản với định dạng cột
    header = df.columns.tolist()
    formatted_header = " | ".join(f"{col:<20}" for col in header)
    separator = "-" * len(formatted_header)
    
    rows = []
    for index, row in df.iterrows():
        formatted_row = " | ".join(f"{str(value):<20}" for value in row)
        rows.append(formatted_row)
    
    output = f"{formatted_header}\n{separator}\n" + "\n".join(rows)
    return output

def format_dataframe_as_text(df):
    # Căn chỉnh chiều rộng cột tối đa
    col_widths = {col: max(df[col].astype(str).map(len).max(), len(col)) for col in df.columns}
    
    
    # Tạo tiêu đề
    header = " | ".join(f"{col:<{col_widths[col]}}" for col in df.columns)
    separator = "-".join("-" * col_widths[col] for col in df.columns)
    
    # Tạo các hàng dữ liệu
    rows = []
    for _, row in df.iterrows():           
        # for col in df.columns:
        #     if col == 'Price Coin (USD)     ':
        #         print(round(row[col], 4))
        #     else:
        #         print(row[col])         
        # formatted_row = " | ".join(f"{str(row[col]):<{col_widths[col]}}" for col in df.columns)
            # text_len = len(row[col])
            # len_txt = 28 - text_len
        formatted_row = " | ".join(
            f"{(round(row[col], 4) if col == 'Price Coin (USD)     ' else str(row[col])):<{col_widths[col]}}"
            for col in df.columns
        )

        rows.append(formatted_row)
    
    # Kết hợp tất cả vào văn bản
    output = f"{header}\n{separator}\n" + "\n".join(rows)
    return output
def main():
    offset = None

    while True:
        updates = get_updates(token, offset)
        for update in updates.get('result', []):
            message = update.get('message')
            if message:
                handle_message(message)
                offset = update['update_id'] + 1
        time.sleep(1)
        
def market_cap():
    while True:
        chat_id = "-4272801743"  # Thay thế bằng chat_id của bạn
        data = get_cryptocurrency_data(api_key)
        
        # Chuyển dữ liệu thành bảng
        df = convert_data_to_dataframe(data)
        
        # # Lưu DataFrame vào file CSV
        # csv_file_path = 'cryptocurrency_data.csv'
        # save_dataframe_to_csv(df, csv_file_path)
        
        # Chuyển DataFrame thành văn bản
        text = format_dataframe_as_text(df)
        
        # Gửi file CSV qua Telegram
        send_message(token, chat_id, text)
        
        # Đợi 10 phút (600 giây) trước khi gửi lại yêu cầu
        time.sleep(600)

if __name__ == '__main__':
    main()
    # market_cap()
