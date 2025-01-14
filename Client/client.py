import socket
from fonctionnalite import *


def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Adresse IP du serveur provisoire
    hote = "127.0.0.1"
    # Port du serveur
    port = 12345
    id_client = " "  # identifiant du clien pour les prochaines manipulaitons
    try:
        # Connexion au serveur
        client_socket.connect((hote, port))
        print(f"Connecté au serveur {hote}:{port}")

        # Connexion au compte utilisateur ou administrateur
        while True:
            choix_initial = afficher_menu_initial()
            if choix_initial == 1:
                # Connexion compte administrateur
                print("Connexion autant qu'administrateur : ")
                res, id = connexion_compte(client_socket)
                # Vérification de si l'utilisateur est bien l'administrateur
                if id != 1:
                    print("Le compte saisie n'est pas un compte administrateur !")
                else:
                    # Si c'est bien un administrateur
                    while True:
                        choix_administrateur = afficher_menu_administrateur()
                        if choix_administrateur == 1:
                            res, id_client = creation_compte(client_socket)
                            if res:
                                # CREATION COMPTE
                                print("Le compte utilisateur a été créé avec succès.")
                            else:
                                print("Le compte n'a pas pu être créé.")
                        if choix_administrateur == 4:
                            print("Déconnexion")
                            break
                        continue

            elif choix_initial == 2:
                # Connexion autant qu'utilisateur
                print("Connexion autant qu'utilisateur : ")
                res, id = connexion_compte(client_socket)
                if res:
                    # CONNEXION CLIENT
                    id_client = id

                    # Affichage du menu principal après connexion
                    while True:
                        # Choix de l'action à effectuer
                        choix = afficher_menu()

                        if choix == 1:
                            print("Ajouter d'un contact à mon annuaire")
                            ajouter_contact(client_socket, id_client)
                        elif choix == 2:
                            print("Modification d'un contact de mon annuaire")
                        elif choix == 3:
                            print("Supprimer un contact de mon annuaire")
                        elif choix == 4:
                            print("Consulter mon annuaire")
                        elif choix == 5:
                            print(
                                "Vous voulez consulter les information d'un contact de votre annuaire:"
                            )
                            Nom = str(input("Veuillez saisir son nom :"))
                            Prenom = str(input("Veuillez saisir son prenom :"))
                            reponse = recherche_contact(
                                Nom, Prenom, client_socket, id
                            )  # emmagasiner l'id dans le code
                            # Traiter la réponse reçue
                            if reponse["code_erreur"] == "0":
                                afficher_info(reponse["donnee"])
                            else:
                                message_erreur = interprete_code_erreur(
                                    int(reponse["code_erreur"])
                                )
                                print(
                                    f"Erreur ({reponse['code_erreur']}) : {message_erreur}"
                                )
                        elif choix == 6:
                            print("Consulter l'annuaire d'une tiers personne")
                        elif choix == 7:
                            print("Donner une Autorisation à un Contact")
                        elif choix == 8:
                            print("Déconnexion")
                            break
                        else:
                            print("Choix invalide. Veuillez réessayer.")

            else:
                print("Choix invalide. Veuillez réessayer.")

        # Envoi d'un message de déconnexion au serveur
        message = "DECONNEXION"
        client_socket.send(message.encode("utf-8"))

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        # Fermeture de la connexion au serveur
        client_socket.close()
        print("Connexion fermée.")


if __name__ == "__main__":
    client()
