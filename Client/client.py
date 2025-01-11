import socket
from fonctionnalite import *

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Adresse IP du serveur provisoire
    hote = '127.0.0.1' 
    # Port du serveur
    port = 12345  
    id_client=" " #identifiant du clien pooru les prochaine manipulaiton
    try:
        # Connexion au serveur
        client_socket.connect((hote, port))
        print(f"Connecté au serveur {hote}:{port}")

        #Connexion a sont compte ou creation de compte 
        while True:
            choix_initial = afficher_menu_initial()
            if choix_initial == 1:
                if 2==2:
                    #CREATION DE COMPTE 
                    #Peut etre mettre l'id que le serveur a attribuer au client dans une valiable ici ??
                    continue
            elif choix_initial == 2:
                res,id=connexion_compte(client_socket)
                if res:
                    #CONNEXION CLIENT 
                    id_client=id
                    #J'ai ecirt un prmeir coe de connectoo doi on prendre en compte le fait que un administrateur se connecte ?
                    break
            else:
                print("Choix invalide. Veuillez réessayer.")

        # Affichage du menu principal après connexion
        while True:
            choix = afficher_menu()

            if choix == 1:
                print("Ajouter d'un contact à mon annuaire")
                # ccode/fonction
            elif choix == 2:
                print("Modification d'un contact de mon annuaire")
                # ccode/fonction
            elif choix == 3:
                print("Supprimer un contact de mon annuaire")
                # ccode/fonction
            elif choix == 4:
                print("Consulter mon annuaire")
                # ccode/fonction
            elif choix == 5:

                print("Vous voulez consulter les information d'un contact de votre annuaire:")
                Nom=str(input("Veuillez saisir son nom :"))
                Prenom=str(input("Veuillew saisir son prenom :"))
                reponse=recherche_contact(Nom, Prenom, client_socket,id)#emmagasiner l'id dans le code
                 # Traiter la réponse reçue
                if reponse["code_erreur"] == "0":
                    print(reponse["donnee"])#peut etre mettre une fonction d'affcihage 
                else:
                    message_erreur = interprete_code_erreur(int(reponse["code_erreur"]))
                    print(f"Erreur ({reponse["code_erreur"]}) : {message_erreur}")
            elif choix == 6:
                print("Consulter l'annuaire d'une tiers personne")
                # ccode/fonction
            elif choix == 7:
                print("Donner une Autorisation à un Contact")
                # ccode/fonction
            elif choix == 8:
                print("Déconnexion")
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

        # Envoi d'un message de déconnexion au serveur
        message = "DECONNEXION"
        client_socket.send(message.encode('utf-8'))

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        # Fermeture de la connexion au serveur
        client_socket.close()
        print("Connexion fermée.")
if __name__ == "__main__":
    client()
