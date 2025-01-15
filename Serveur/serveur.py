import socket
import threading
import json
from fonctionnalites import traiter_requete, charger_annuaire, sauvegarder_annuaire

# Configuration du serveur
HOTE = "127.0.0.1"  # Adresse IP du serveur
PORT = 12344  # Port du serveur
TAILLE_BUFFER = 1024  # Taille du buffer pour les messages

# Chargement de l'annuaire (par exemple, à partir d'un fichier JSON)
annuaire = charger_annuaire()

# Indicateur pour arrêter le serveur
server_running = True


def gerer_client(client_socket, adresse_client):
    """
    Gère la communication avec un client spécifique.
    """
    print(f"Connexion établie avec {adresse_client}")
    try:
        while True:
            # Réception de la requête du client
            data = client_socket.recv(TAILLE_BUFFER).decode("utf-8")
            if not data:  # Si aucune donnée reçue, déconnexion
                break

            print(f"Requête reçue de {adresse_client} : {data}")

            # Traitement de la requête
            reponse = traiter_requete(data, annuaire)

            # Vérification si le client demande la déconnexion
            if json.loads(data)["type_action"].upper() == "DECONNEXION":
                print(f"Le client {adresse_client} s'est déconnecté.")
                break  # Sortir de la boucle pour ce client
            print("Envoi de la response...")
            # Envoi de la réponse au client
            client_socket.sendall(reponse.encode("utf-8"))

    except Exception as e:
        print(f"Erreur avec le client {adresse_client} : {e}")
    finally:
        print(f"Déconnexion du client {adresse_client}")
        client_socket.close()


def demarrer_serveur():
    """
    Démarre le serveur et accepte les connexions entrantes.
    """
    global server_running

    serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur_socket.bind((HOTE, PORT))
    serveur_socket.listen(5)  # Le serveur peut gérer jusqu'à 5 connexions en file d'attente
    print(f"Serveur démarré sur {HOTE}:{PORT}")

    # Thread pour accepter les connexions
    def accepter_connexions():
        while server_running:
            try:
                client_socket, adresse_client = serveur_socket.accept()
                print(f"Nouveau client connecté : {adresse_client}")
                # Gestion du client dans un thread séparé
                thread_client = threading.Thread(
                    target=gerer_client, args=(client_socket, adresse_client)
                )
                thread_client.start()
            except Exception as e:
                if server_running:
                    print(f"Erreur lors de l'acceptation de connexion : {e}")

    thread_connexions = threading.Thread(target=accepter_connexions)
    thread_connexions.start()

    # Interface de commande pour arrêter le serveur
    try:
        while True:
            commande = input("Entrez 'stop' pour arrêter le serveur : ").strip().lower()
            if commande == "stop":
                print("Arrêt du serveur demandé...")
                server_running = False
                break
    except KeyboardInterrupt:
        print("Arrêt du serveur via Ctrl+C.")
    finally:
        # Sauvegarde de l'annuaire avant l'arrêt du serveur
        sauvegarder_annuaire(annuaire)
        serveur_socket.close()
        thread_connexions.join()
        print("Serveur arrêté proprement.")

if __name__ == "__main__":
    demarrer_serveur()