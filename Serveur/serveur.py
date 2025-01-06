import socket

def serveur():
    # Création du socket
    serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hote = '127.0.0.1'  # Adresse IP locale
    port = 12345  # Port sur lequel le serveur écoute

    # Liaison du socket à l'adresse et au port
    serveur_socket.bind((hote, port))
    # Le serveur peut accepter jusqu'à 5 connexions
    serveur_socket.listen(5)  
    print(f"Serveur en attente de connexion sur {hote}:{port}...")


    while True:
        client_socket, adresse_client = serveur_socket.accept()
        print(f"Connexion acceptée de {adresse_client}")

        # Rception d'une réponse au client
        message = client_socket.recv(1024).decode('utf-8')
        print(f"Message reçu du client : {message}")



        # Envoi d'une réponse au client
        client_socket.send("Message reçu avec succès".encode('utf-8'))

        # Fermeture de la connexion avec le client
        client_socket.close()

if __name__ == "__main__":
    serveur()


#accept()                               : accepte une connexion, retourne un nouveau socket et une adresse client 
#bind(addr)                             : associe le socket à une adresse locale
#close()                                : ferme le socket
#connect(addr)                          : connecte le socket à une adresse distante 
#connect_ex(addr)                       : connect, retourne un code erreur au lieu d'une exception
#dup()                                  : retourne un nouveau objet socket identique à celui en cours
#fileno()                               : retourne une description du fichier
#getpeername()                          : retourne l'adresse distante
#getsockname()                          : retourne l'adresse locale
#getsockopt(level, optname[, buflen])   : retourne les options du socket
#gettimeout()                           : retourne le timeout ou none
#listen(n)                              : commence à écouter les connexions entrantes
#makefile([mode, [bufsize]])            : retourne un fichier objet pour le socket
#recv(buflen[, flags])                  : recoit des données
#recv_into(buffer[, nbytes[, flags]])   : recoit des données (dans un buffer)
#recvfrom(buflen[, flags])              : reçoit des données et l'adresse de l'envoyeur
#recvfrom_into(buffer[,nbytes,[,flags]) : reçoit des données et l'adresse de l'envoyeur (dans un buffer)
#sendall(data[, flags])                 : envoye toutes les données
#send(data[, flags])                    : envoye des données mais il se peut que pas toutes le soit
#sendto(data[, flags], addr)            : envoye des données à une adresse donnée
#setblocking(0 | 1)                     : active ou désactive le blocage le flag I/O
#setsockopt(level, optname, value)      : définit les options du socket
#settimeout(None | float)               : active ou désactive le timeout
#shutdown(how) 