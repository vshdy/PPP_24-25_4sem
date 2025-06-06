1. Если вдруг слетели зависимости:
sudo chown -R $USER:$USER ~/Mirach_laba3 - открыть доступ
sudo python3 -m venv venv
sudo apt update
sudo apt install python3.12-venv
source venv/bin/activate
pip install -r requirements.txt
pip install pydantic[email]

2. каждом из трех войдем в директории и активируем вирт прсотранство

cd ~/Mirach_laba3
source venv/bin/activate
2.1 первый терминал для селери:
 celery -A celery_worker worker --loglevel=info
2.2 второй для ювикорна:
uvicorn main:app --reload

websocket king: ws://127.0.0.1:8000/ws/13 - для получения уведомлний
2.3 третий терминал клиента
python3 client.py