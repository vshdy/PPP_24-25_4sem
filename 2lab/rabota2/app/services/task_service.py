import os
import string
import subprocess
from celery import Celery
from itertools import product
import logging
import rarfile

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

rar2john_path = "C:/Users/user/Documents/john-1.9.0-jumbo-1-win64/john-1.9.0-jumbo-1-win64/run/rar2john.exe"

celery_app = Celery("task_service", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

@celery_app.task
def brute_force_task(task_id: int, rar_path: str, charset: str, max_length: int):
    from app.db.session import SessionLocal
    from app.models.task_model import Task

    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logging.error("Не найдена задача с таким task_id")
        return None

    logging.debug(f"Начинается брутфорс для архива: {rar_path}, charset={charset}, max_length={max_length}")
    
    try:
        rar2john_result = subprocess.run(
            [rar2john_path, rar_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        extracted_hash = rar2john_result.stdout.decode("utf-8").strip()
        logging.debug(f"Извлеченный хэш из архива: {extracted_hash}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при извлечении хэша через rar2john: {e}")
        task.status = "failed"
        db.commit()
        return None

    wordlist_file = os.path.join(os.getcwd(), "wordlist.txt")
    with open(wordlist_file, "w") as f:
        for length in range(1, max_length + 1):
            for combo in product(charset, repeat=length):
                password = ''.join(combo)
                f.write(password + "\n")
    logging.debug(f"Сгенерирован файл словаря: {wordlist_file}")

    found_password = None
    total_tests = 0
    with open(wordlist_file, "r") as f:
        for password in f:
            password = password.strip()
            total_tests += 1
            try:
                logging.debug(f"Проверка пароля: {password} (Тест {total_tests})")
                total_combinations = sum([len(list(product(charset, repeat=length))) for length in range(1, max_length + 1)])

                for total_tests, password in enumerate(f, start=1):
                    if total_tests % 100 == 0: 
                        task.progress = (total_tests / total_combinations) * 100
                        db.commit()                
                rf = rarfile.RarFile(rar_path)
                infos = rf.infolist()
                if not infos:
                    logging.error("Архив пустой или поврежден.")
                    task.status = "failed"
                    task.result = None
                    db.commit()
                    return None
                project_dir = os.path.dirname(os.path.abspath(__file__)) 
                extract_dir = os.path.join(project_dir, "extracted_files")
                os.makedirs(extract_dir, exist_ok=True)  

                logging.debug(f"Пытаемся извлечь файл в {extract_dir} с паролем {password}")
                rf.extract(infos[0], path=extract_dir, pwd=password)
                found_password = password
                logging.debug(f"[УСПЕХ] Пароль найден: {found_password} после {total_tests} попыток")
                break
            except rarfile.BadRarFile as e:
                logging.error(f"Ошибка с архивом: {e}")
                task.status = "failed"
                task.result = None
                db.commit()
                return None
            except rarfile.RarWrongPassword:
                logging.debug(f"Пароль неверный: {password}")
                continue
            except Exception as e:
                logging.error(f"Непредвиденная ошибка при проверке пароля {password}: {e}")
                continue

    if found_password:
        task.status = "completed"
        task.result = found_password
        db.commit()
    else:
        task.status = "failed"
        task.result = None
        db.commit()

    return found_password
