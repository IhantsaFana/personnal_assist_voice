# Configuration Gunicorn pour Render.com
import multiprocessing

# Configuration du worker
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
threads = 2

# Timeouts
timeout = 120
keepalive = 5

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
