# Configuration Gunicorn pour Render.com
import multiprocessing
import os

# Configuration du worker
workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2))
worker_class = "gevent"
worker_connections = 1000
threads = int(os.getenv("PYTHON_MAX_THREADS", 4))

# Timeouts
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Bind - Render définit la variable PORT
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# En-têtes de sécurité
forwarded_allow_ips = "*"
secure_scheme_headers = {"X-Forwarded-Proto": "https"}

# Logging
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = "-"
loglevel = "info"

# Bind
bind = "0.0.0.0:$PORT"

# SSL/HTTPS
forwarded_allow_ips = "*"
secure_scheme_headers = {
    "X-FORWARDED-PROTO": "https",
}
