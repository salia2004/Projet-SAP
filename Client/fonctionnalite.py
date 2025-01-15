import socket as s
import json


# ------------------------------------------------------
# ---- Fonctions d'affichage
# ------------------------------------------------------
def demander_identifiants():
    identifiant = input("Email : ")
    mot_de_passe = input("Mot de passe : ")
    return identifiant, mot_de_passe


def afficher_menu_initial():
    try:
        print(" ------ Menu Initial ------ \n\n")
        print("1- Se connecter à un compte administrateur")
        print("2- Se connecter à un compte utilisateur")
        print("3- Quitter l'application")
        choix = int(input("Veuillez renseigner votre choix : "))
        return choix
    except ValueError:
        print("Veuillez entrer un nombre entier.")


def afficher_menu():
    try:
        print(" ------ Menu principale ------ \n\n")
        print("1- Ajouter un contact à mon annuaire")
        print("2- Modifier un contact de mon annuaire")
        print("3- Supprimer un contact de mon annuaire")
        print("4- Consulter mon annuaire")
        print("5- Consulter un contact spécifique de mon annuaire")
        print("6- Consulter l'annuaire d'une tiers personne")
        print("7- Donner une Autorisation à un Contact ")
        print("8- Deconnexion")
        choix = int(input("Veuillez renseignez votre choix : "))
        return choix
    except ValueError:
        print("Veuillez entrer un nombre entier.")


def afficher_menu_administrateur():
    try:
        print(" ------ Menu Administrateur ------ \n\n")
        print("1- Ajouter un compte utilisateur")
        print("2- Modifier un compte utilisateur")
        print("3- Supprimer un compte utilisateur")
        print("4- Deconnexion")

        choix = int(input("Veuillez renseignez votre choix : "))
        return choix
    except ValueError:
        print("Veuillez entrer un nombre entier.")


"""
Affiche les informations d'un contact de manière claire et structurée.
    :param contact: Dictionnaire contenant les informations d'un contact.
"""


def afficher_info(contact):
    print("\n------ Informations du Contact ------")
    for elem in contact:
        print(f"Nom                : {elem.get('Nom', 'Non spécifié')}")
        print(f"Prénom             : {elem.get('Prenom', 'Non spécifié')}")
        print(f"Email              : {elem.get('Email', 'Non spécifié')}")
        print(f"Adresse postale    : {elem.get('Adresse postale', 'Non spécifié')}")
        print(
            f"Numéro de téléphone: {elem.get('Numéro de téléphone', 'Non spécifié')}\n"
        )


# ------------------------------------------------------
# ------------------------------------------------------
"""
Permet a partir de la reponse envoyer par le serveur d'interpreter l'erreur
"""


def interprete_code_erreur(code):
    codes_erreurs = {
        400: "Requête mal formulée.",
        401: "Authentification requise.",
        402: "Informations obligatoires manquantes.",
        403: "Contact déjà présent dans l’annuaire.",
        404: "Contact non trouvé.",
        405: "Adresse mail déjà présente.",
        406: "Identifiants incorrects.",
        407: "Mot de passe incorrect.",
        408: "Accès refusé.",
        409: "Utilisateur non trouvé.",
    }
    return codes_erreurs.get(code, "Erreur inconnue.")


"""
Fonctionnalité CONNEXION
Objectif: Permet a un utilisateur de se connecter a son compte en renseignant ses addresse mail et sont mdp
"""


def connexion_compte(client_socket):
    fin = False
    compteur = 0  # 2 tentative autoriser
    while not fin and compteur < 2:
        # Collecter les informations de l'utilisateur
        email, mot_de_passe = demander_identifiants()

        # Création de la requête directement en dictionnaire
        requete = {
            "type_message": "requete",
            "type_action": "CONNEXION",
            "identifiant": None,
            "donnee": {"email": email, "mdp": mot_de_passe},
            "code_erreur": None,
        }
        client_socket.sendall(json.dumps(requete).encode("utf-8"))

        reponse_data = client_socket.recv(1024).decode("utf-8")
        reponse = json.loads(reponse_data)

        # Traiter la réponse reçue
        if reponse["code_erreur"] == "0":
            print("Connexion établie avec succès.")
            id = reponse["donnee"]["id"]
            fin = True
        else:
            message_erreur = interprete_code_erreur(int(reponse["code_erreur"]))
            print(f"Erreur ({reponse['code_erreur']}) : {message_erreur}")
            print("Veuillez reessayer")
            compteur = compteur + 1
    if compteur >= 3:
        return False, " "
    return fin, id
"""
Fonctionnalité recherche_contact 
Objectif: Permet a un utilisateur de rechercher un contact de son annuaire en reseingnant les information du contact (Nom et Prenom)
Parametre: 
    Nom: char 
    Prenom : char
    socket : socket 
Auteur: Fatoumata Salia Traore 
"""


def recherche_contact(Nom, Prenom, socket, id):
    try:
        # Création de la requete
        requete = {
            "type_message": "requete",
            "type_action": "CONSULTER_CONTACT",
            "identifiant": id,
            "donnee": {"nom": Nom, "prenom": Prenom},
            "code_erreur": None,
        }

        # Envoi de la requête au serveur via le socket
        socket.sendall(json.dumps(requete).encode("utf-8"))

        # Réception de la réponse du serveur
        reponse_data = socket.recv(1024).decode("utf-8")
        reponse = json.loads(reponse_data)
        return reponse
    except Exception as e:
        print(f"Erreur lors de la recherche du contact : {e}")
        return None


"""
Fonctionnalité AJOUTER_CONTACT
Objectif: Permet à un utilisateur d'ajouter un nouveau contact à son annuaire.
Paramètres:
    socket : socket
    id : identifiant de l'utilisateur connecté
"""


def ajouter_contact(socket, id):
    try:
        # Collecte des informations du contact à ajouter
        print("\n--- Ajouter un contact ---")
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        email = input("Email : ")
        adresse_postale = input("Adresse postale : ")
        numero_telephone = input("Numéro de téléphone : ")

        # Création de la requête à envoyer au serveur
        requete = {
            "type_message": "requete",
            "type_action": "AJOUT_CONTACT",
            "identifiant": id,
            "donnee": {
                "Nom": nom,
                "Prenom": prenom,
                "Email": email,
                "Adresse postale": adresse_postale,
                "Numéro de téléphone": numero_telephone,
            },
            "code_erreur": None,
        }

        # Envoi de la requête au serveur
        socket.sendall(json.dumps(requete).encode("utf-8"))

        # Réception de la réponse du serveur
        reponse_data = socket.recv(1024).decode("utf-8")
        reponse = json.loads(reponse_data)

        # Traitement de la réponse
        if reponse["code_erreur"] == "0":
            print("Contact ajouté avec succès !")
        else:
            message_erreur = interprete_code_erreur(int(reponse["code_erreur"]))
            print(f"Erreur ({reponse['code_erreur']}) : {message_erreur}")
    except Exception as e:
        print(f"Erreur lors de l'ajout du contact : {e}")


"""
Fonctionnalité CREATION_COMPTE
Objectif: Permet à l'administrateur de créer un compte utilisateur
Paramètres:
    socket : socket
Auteur : Amina DIDANE
"""


def creation_compte(socket):
    try:
        # Collecte des informations de l'utilisateur à ajouter
        print("\n--- Création utilisateur ---")
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        email = input("Mail : ")
        mot_de_passe = input("Mot de passe : ")

        # Création de la requête à envoyer au serveur
        requete = {
            "type_message": "requete",
            "type_action": "CREATION_COMPTE",
            "identifiant": None,
            "donnee": {
                "nom": nom,
                "prenom": prenom,
                "email": email,
                "mdp": mot_de_passe,
                "annuaire_contact": [],
            },
            "code_erreur": None,
        }

        # Envoi de la requête au serveur
        socket.sendall(json.dumps(requete).encode("utf-8"))

        # Réception de la réponse du serveur
        reponse_data = socket.recv(1024).decode("utf-8")
        reponse = json.loads(reponse_data)

        # Traitement de la réponse
        if reponse["code_erreur"] == "0":
            print("Utilisateur ajouté avec succès !")
            return True, reponse["donnee"]["id_client"]
        else:
            message_erreur = interprete_code_erreur(int(reponse["code_erreur"]))
            print(f"Erreur ({reponse['code_erreur']}) : {message_erreur}")
            return False, None
    except Exception as e:
        print(f"Erreur lors de la création d'un compte utilisateur : {e}")
