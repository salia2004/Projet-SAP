import socket
import threading
import json
from fonctionnalites import traiter_requete, charger_annuaire, sauvegarder_annuaire

# Configuration du serveur
HOTE = '127.0.0.1'  # Adresse IP du serveur
PORT = 12345        # Port du serveur
TAILLE_BUFFER = 1024  # Taille du buffer pour les messages

# Chargement de l'annuaire (par exemple, à partir d'un fichier JSON)
annuaire = charger_annuaire()

def gerer_client(client_socket, adresse_client):
    """
    Gère la communication avec un client spécifique.
    """
    print(f"Connexion établie avec {adresse_client}")
    try:
        while True:
            # Réception de la requête du client
            data = client_socket.recv(TAILLE_BUFFER).decode('utf-8')
            if not data:  # Si aucune donnée reçue, déconnexion
                break

            print(f"Requête reçue de {adresse_client} : {data}")
            
            # Traitement de la requête
            reponse = traiter_requete(data, annuaire)
            print("Envoi de la response...")
            # Envoi de la réponse au client
            client_socket.sendall(reponse.encode('utf-8'))

            #traiter le cas de deconnection de la par du client ici ausi
    except Exception as e:
        print(f"Erreur avec le client {adresse_client} : {e}")
    finally:
        print(f"Déconnexion du client {adresse_client}")
        client_socket.close()

def demarrer_serveur():
    """
    Démarre le serveur et accepte les connexions entrantes.
    """
    serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur_socket.bind((HOTE, PORT))
    serveur_socket.listen(5)  # Le serveur peut gérer jusqu'à 5 connexions en file d'attente
    print(f"Serveur démarré sur {HOTE}:{PORT}")

    try:
        while True:
            # Acceptation d'une nouvelle connexion client
            client_socket, adresse_client = serveur_socket.accept()
            print(f"Nouveau client connecté : {adresse_client}")

            # Gestion du client dans un thread séparé
            thread_client = threading.Thread(target=gerer_client, args=(client_socket, adresse_client))
            thread_client.start()
    except KeyboardInterrupt:
        print("Arrêt du serveur.")
    finally:
        # Sauvegarde de l'annuaire avant l'arrêt du serveur
        sauvegarder_annuaire(annuaire) #implementer dans fonctionnaliter 
        serveur_socket.close()

if __name__ == "__main__":
    demarrer_serveur()
