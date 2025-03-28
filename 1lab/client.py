import socket
import json

'''
• Устанавливает сетевое взаимодействие с сервером.
• Позволяет пользователю выполнять следующие команды:
• Получить список доступных аудиофалов.
• Запросить отрезок аудиодорожки, указав имя файла, начальное и конечное время (в секундах)
• Получает от сервера запрошенный отрезок аудио и сохраняет его локально.

'''

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

def get_audio_list(client_socket):
    client_socket.send('LIST'.encode())
    data = client_socket.recv(4096).decode()
    audio_list = json.loads(data)
    return audio_list

def request_audio_segment(client_socket, file_name, start, end):
    request = f'GET {file_name} {start} {end}'
    client_socket.send(request.encode())
    
    header = client_socket.recv(10).decode()
    try:
        file_size = int(header)
    except ValueError:
        print("Ошибка при получении размера файла")
        return
    
    remaining = file_size
    with open(f"downloaded_{file_name}", 'wb') as f:
        while remaining > 0:
            chunk = client_socket.recv(min(1024, remaining))
            if not chunk:
                break
            f.write(chunk)
            remaining -= len(chunk)
    print(f"Аудио сегмент сохранен как downloaded_{file_name}")

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        print("Подключено к серверу")
        
        while True:
            print("\nКоманды:")
            print("1 - Получить список файлов")
            print("2 - Запросить аудио сегмент")
            print("q - Выйти")
            command = input("Выберите опцию: ")

            if command == '1':
                audio_list = get_audio_list(client_socket)
                print("\nДоступные аудио файлы:")
                for i, audio in enumerate(audio_list):
                    print(f"{i+1}. {audio['name']} (Длительность: {audio['duration']}с, формат: {audio['format']})")
            
            elif command == '2':
                audio_list = get_audio_list(client_socket)
                print("\nДоступные аудио файлы:")
                for i, audio in enumerate(audio_list):
                    print(f"{i+1}. {audio['name']} (Длительность: {audio['duration']}с, формат: {audio['format']})")
                
                file_choice = int(input("Выберите номер файла: ")) - 1
                file_name = audio_list[file_choice]['name']
                start = int(input("Введите время начала сегмента: "))
                end = int(input("Введите время конца сегмента: "))

                request_audio_segment(client_socket, file_name, start, end)

            elif command == 'q':
                print("Выход совершен")
                break

if __name__ == "__main__":
    start_client()
