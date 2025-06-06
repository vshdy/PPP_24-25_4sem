from redislite import Redis

redis = Redis("/tmp/redislite_lab.db")
redis_socket_path = redis.socket_file
