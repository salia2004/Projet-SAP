import socket
from fonctionnalite import *




def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Adresse IP du serveur provisoire
    hote = '127.0.0.1' 
    # Port du serveur
    port = 12345  

    try:
        # Connexion au serveur
        client_socket.connect((hote, port))
        print(f"Connecté au serveur {hote}:{port}")

        #Partie connection ou creation de compte 


        # Envoi d'un message au serveur
        message = "Bonjour, serveur!"
        client_socket.send(message.encode('utf-8'))

        # Réception de la réponse du serveur
        reponse = client_socket.recv(1024).decode('utf-8')
        print(f"Réponse du serveur : {reponse}")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        # Fermeture de la connexion au serveur
        client_socket.close()



if __name__ == "__main__":
    client()