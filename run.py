import socket
import uvicorn


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))
    
    host = sock.getsockname()[0]
except:
    host = '127.0.0.1'
finally:
    sock.close()
    
port = 80


uvicorn.run(
    'app:app',
    host=host,
    port=port
)