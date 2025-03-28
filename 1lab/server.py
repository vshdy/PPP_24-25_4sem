import os
import json
import socket
import threading
import logging
import tempfile
from pydub import AudioSegment 

'''
• Хранит набор аудиофайлов в определенной директории.
• Использует модуль os для работы с файловой системой.
• При запуске создает и сохраняет в JSON-файл список всех аудиофайлов с их метаданными (имя файла, длительность, формат).
• Ожидает подключения клиентов и обрабатывает их запросы.
• Обрабатывает запросы на получение списка аудиофайлов.
• Вырезает указанный отрезок из аудиофайла, используя временные файлы.
• Отправляет клиенту запрошенный отрезок аудио.
• Обеспечивает многопоточную обработку для одновременной работы с несколькими клиентами



• Использовать библиотеку pydub для работы с аудиофайлами.
• Применять модуль tempfile для создания и управления временными файлами.
• Реализовать базовое логирование действий сервера и клиента.

'''

AUDIO_DIR = "audio_files"  
METADATA_FILE = "metadata.json"  
HOST = "127.0.0.1" 
PORT = 5000 


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def scan_audio_files():
    metadata = [] 

    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    for file in os.listdir(AUDIO_DIR):
        if file.endswith((".mp3", ".wav")):
            filepath = os.path.join(AUDIO_DIR, file)
            audio = AudioSegment.from_file(filepath) 
            metadata.append({
                "name": file,
                "duration": len(audio) / 1000, 
                "format": file.split(".")[-1] 
            })

    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f)

    logging.info("Обновлён список аудиофайлов.")






def handle_client(conn, addr):
    logging.info(f"Новое подключение: {addr}")

    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break 

            logging.info(f"Получен запрос от {addr}: {data}")
            parts = data.split()

            if parts[0] == "LIST":
                with open(METADATA_FILE, "r") as f:
                    files = f.read()  
                conn.sendall(files.encode())

            elif parts[0] == "GET" and len(parts) == 4:
                filename, start, end = parts[1], int(parts[2]), int(parts[3])
                filepath = os.path.join(AUDIO_DIR, filename)
                temp_folder = "C:/Users/Public/Temp"

                if not os.path.exists(temp_folder):
                    os.makedirs(temp_folder)
                if os.path.exists(filepath):
                    audio = AudioSegment.from_file(filepath)
                    if 0 <= start < end <= len(audio) / 1000:
                        with tempfile.NamedTemporaryFile(dir=temp_folder, delete=0, suffix=".mp3") as temp_audio: 
                            segment = audio[start * 1000:end * 1000]  
                            segment.export(temp_audio.name, format="mp3")
                            temp_filename = temp_audio.name

                            file_size = os.path.getsize(temp_filename)
                            header = str(file_size).zfill(10).encode()
                            conn.sendall(header)

                            with open(temp_filename, "rb") as f:
                                conn.sendall(f.read())

                        logging.info(f"Отправлен фрагмент {filename} ({start}-{end} сек.) клиенту {addr}")
                        os.remove(temp_filename)
                    else:
                        conn.sendall(b"ERROR: wrong period of time")
                else:
                    conn.sendall(b"ERROR: can t find the file")

            else:
                conn.sendall(b"ERROR: wrong command")

        except Exception as e:
            logging.error(f"Ошибка при обработке запроса: {e}")
            break

    conn.close()
    logging.info(f"Клиент {addr} отключился")





def start_server():
    scan_audio_files()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT)) 
    server.listen(5)
    logging.info(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()  
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start() 



if __name__ == '__main__':
    start_server()



















