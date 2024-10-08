import fnmatch
import logging
import signal
import socket
import sys
import threading
import socket
from time import localtime, strftime
import colorizePython
class Server:
    def __init__(self, config) -> None:
        # pour pouvoir arrêter avec un Ctrl + C
        signal.signal(signal.SIGINT, self.shutdown)

        # Correction: socket.scocket -> socket.socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Réutiliser le socket
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Lier le socket à un hôte public et à un port
        self.serverSocket.bind((config['HOST_NAME'], config['BIND_PORT']))

        self.serverSocket.listen(10)  # devenir un socket serveur

        self.clients = {}
        while True:
            # Établir la connexion
            (clientSocket, client_address) = self.serverSocket.accept()
            d = threading.Thread(target=self.proxy_thread, args=(clientSocket, client_address))
            d.setDaemon(True)
            d.start()
    def test():
        try:
            ip = socket.gethostbyname('example.com')
            print(f"IP address of example.com: {ip}")
        except socket.gaierror as e:
            print(f"Error resolving example.com: {e}")

    def proxy_thread(self, conn,client_address):
        config = {
            'MAX_REQUEST_LEN': 4096,  # La taille maximale de la requête, à définir dans le fichier de configuration
            'CONNECTION_TIMEOUT': 5,  # Le délai d'attente, à définir aussi dans le fichier de config
        }

        # Obtenir la requête depuis le navigateur
        request = conn.recv(config['MAX_REQUEST_LEN'])

        # Analyser la première ligne
        first_line = request.decode().split('\n')[0]
        print(first_line)
        # Obtenir l'URL
        url = first_line.split(' ')[1]

        http_pos = url.find("://")  # Trouver le pos de ://
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]  # Obtenir le reste de l'url

        port_pos = temp.find(":")  # Trouver le port pos (le cas échéant)

        # Trouver la fin du serveur web
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        
        if port_pos == -1 or webserver_pos < port_pos:
            # Port par défaut
            port = 80
            webserver = temp[:webserver_pos]
        else:
            # Port spécifique
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        try:
            print(f"Connecting to webserver: {webserver} on port: {port}")
            # Se connecter au serveur web distant
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((webserver, port))
            s.sendall(request)
            # s.settimeout(config['CONNECTION_TIMEOUT'])


            while True:
                # Recevoir des données du serveur Web
                data = s.recv(config['MAX_REQUEST_LEN'])

                if len(data) > 0:
                    conn.send(data)  # Envoyer au navigateur/client
                else:
                    break
        finally:
            conn.close()  # Fermer la connexion du client
            s.close()  # Fermer la connexion du serveur distant
    def verify(self,config,conn,url):
        for i in range(0, len(config['BLACKLIST_DOMAINS'])):
            if config['BLACKLIST_DOMAINS'][i] in url:
                conn.close()
        return
    def _ishostAllowed(self, host):

        """ Check if host is allowed to access
            the content """
        for wildcard in config['HOST_ALLOWED']:
            if fnmatch.fnmatch(host, wildcard):
                logging.basicConfig(level = logging.DEBUG,
format = '[%(CurrentTime)-10s] (%(ThreadName)-10s) %(message)s',)
                return True
        return False
    
    def shutdown(self, signum, frame):
        """ Handle the exiting server. Clean all traces """
        self.log("WARNING", -1, 'Shutting down gracefully...')
        main_thread = threading.currentThread() # Wait for all clients to exit
        for t in threading.enumerate():
            if t is main_thread:
                continue
                self.log("FAIL", -1, 'joining ' + t.getName())
            t.join()
            self.serverSocket.close()
        sys.exit(0)
def colorizeLog(shouldColorize, log_level, msg):
        ## Higher is the log_level in the log()
        ## argument, the lower is its priority.
        colorize_log = {
        "NORMAL": colorizePython.pycolors.ENDC,
        "WARNING": colorizePython.pycolors.WARNING,
        "SUCCESS": colorizePython.pycolors.OKGREEN,
        "FAIL": colorizePython.pycolors.FAIL,
        "RESET": colorizePython.pycolors.ENDC
        }

        if shouldColorize.lower() == "true":
            if log_level in colorize_log:
                return colorize_log[str(log_level)] + msg + colorize_log['RESET']
            return colorize_log["NORMAL"] + msg + colorize_log["RESET"]
        return msg 
def log(self, log_level, client, msg):

    """ Log the messages to appropriate place """
    LoggerDict = {
    'CurrentTime' : strftime("%a, %d %b %Y %X", localtime()),
    'ThreadName' : threading.currentThread().getName()
    }
    if client == -1: # Main Thread
        formatedMSG = msg
    else: # Child threads or Request Threads
        formatedMSG = '{0}:{1} {2}'.format(client[0], client[1], msg)
    logging.debug('%s', colorizeLog(config['COLORED_LOGGING'],
    log_level, formatedMSG), extra=LoggerDict)
if __name__ == "__main__":
    # Configuration du serveur
    
    config = {
        'HOST_NAME': 'localhost',  # Écouter sur toutes les interfaces
        'BIND_PORT': 8888,        # Port d'écoute du proxy
        'MAX_REQUEST_LEN': 4096,  # Taille max de la requête
        'CONNECTION_TIMEOUT': 5   # Timeout des connexions
    }

    # Créer une instance de la classe Server avec la configuration
    server = Server(config)
