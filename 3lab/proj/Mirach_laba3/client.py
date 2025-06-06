import requests
import websockets
import asyncio
import json
import threading

BASE_URL = "http://127.0.0.1:8000"

def register():
    print("\nРегистрация")
    email = input("Email: ")
    password = input("Password: ")
    response = requests.post(f"{BASE_URL}/register", json={"email": email, "password": password})
    if response.status_code == 200:
        print("Пользователь успешно зарегистрирован!\n")
    else:
        print("Ошибка регистрации:", response.json()["detail"])

def login():
    print("\n Вход")
    email = input("Email: ")
    password = input("Password: ")
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    if response.status_code == 200:
        data = response.json()
        print("Успешный вход!\n")
        return data["id"], data["token"]
    else:
        print("Ошибка входа:", response.json()["detail"])
        return None, None

async def listen_websocket(user_id):
    uri = f"ws://127.0.0.1:8000/ws/{user_id}"
    try:
        async with websockets.connect(uri) as websocket:
            print("WebSocket подключён! Ожидаем уведомлений...\n")
            async for message in websocket:
                data = json.loads(message)
                print("Уведомление:")
                print(f" Task ID: {data['task_id']}")
                print(f"  Status: {data['status']}")
                print(f"  Progress: {data['progress']}%")
                print(f"  Operation: {data['operation']}")
                if data['status'] == "COMPLETED":
                    print(f"  Result:\n{json.dumps(data['result'], indent=2, ensure_ascii=False)}\n")
                print("-" * 40)
    except Exception as e:
        print("WebSocket ошибка:", e)


def start_ws_listener(user_id):
    asyncio.run(listen_websocket(user_id))

def encode(token):
    print("\nEncode")
    text = input("Введите текст: ")
    key = input("Введите ключ: ")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/encode", json={"text": text, "key": key}, headers=headers)
    if response.status_code == 200:
        print("Задача отправлена. task_id:", response.json()["task_id"])
    else:
        print("Ошибка:", response.text)

import re

def decode(token):
    print("\nDecode")
    encoded = input("Encoded data: ")
    key = input("Key: ")
    padding = int(input("Padding: "))

    print("Введите Huffman-коды (key=value построчно или одну строку из Swagger):")
    huffman_codes = {}

    while True:
        line = input()
        if not line:
            break

        if '"' in line and ":" in line:
            try:
                huffman_codes = json.loads("{" + line + "}")
            except json.JSONDecodeError:
                print("Ошибка парсинга! Убедитесь, что строка в формате: \"key\": \"value\", ...")
                return
            break
        elif "=" in line:
            k, v = line.split("=", 1)
            huffman_codes[k.strip()] = v.strip()
        else:
            print("Некорректный формат. Введите key=value или вставьте Swagger-строку")

    payload = {
        "encoded_data": encoded,
        "key": key,
        "padding": padding,
        "huffman_codes": huffman_codes
    }

    res = requests.post(f"{BASE_URL}/decode", json=payload, headers={"Authorization": f"Bearer {token}"})
    if res.status_code == 200:
        print("Задача отправлена. task_id:", res.json()["task_id"])
    else:
        print("Ошибка при отправке задачи:", res.text)



def main():
    print("Добро пожаловать в клиент шифрования")
    while True:
        action = input("Выберите: [1] Регистрация, [2] Вход, [0] Выход: ")
        if action == "1":
            register()
        elif action == "2":
            user_id, token = login()
            if user_id:
                threading.Thread(target=start_ws_listener, args=(user_id,), daemon=True).start()
                break
        elif action == "0":
            return

    while True:
        cmd = input("\nВыберите: [1] Encode, [2] Decode, [0] Выйти: ")
        if cmd == "1":
            encode(token)
        elif cmd == "2":
            decode(token)
        elif cmd == "0":
            print("До свидания!")
            break

if __name__ == "__main__":
    main()
