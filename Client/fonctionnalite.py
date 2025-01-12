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
    print(" ------ Menu Initial ------ \n\n")
    print("1- Créer un compte")
    print("2- Se connecter à un compte")
    choix = int(input("Veuillez renseigner votre choix : "))
    return choix


def afficher_menu():
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


"""
Affiche les informations d'un contact de manière claire et structurée.
    :param contact: Dictionnaire contenant les informations d'un contact.
"""


def afficher_info(contact):
    print("\n------ Informations du Contact ------")
    print(f"Nom                : {contact.get('Nom', 'Non spécifié')}")
    print(f"Prénom             : {contact.get('Prenom', 'Non spécifié')}")
    print(f"Email              : {contact.get('Email', 'Non spécifié')}")
    print(f"Adresse postale    : {contact.get('Adresse postale', 'Non spécifié')}")
    print(
        f"Numéro de téléphone: {contact.get('Numéro de téléphone', 'Non spécifié')}\n"
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
                "nom": nom,
                "prenom": prenom,
                "email": email,
                "adresse_postale": adresse_postale,
                "numero_telephone": numero_telephone,
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
        # Connexion autant qu'administrateur
        print("Connexion autant qu'administrateur : ")
        res, id = connexion_compte(socket)
        # Vérification de si l'utilisateur est bien l'administrateur
        if id != 1:
            print("La création de compte est réservé à l'administrateur.")
            return False, None

        # Collecte des informations de l'utilisateur à ajouter
        print("\n--- Création utilisateur ---")
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        email = input("Mail : ")
        mot_de_passe = input("Mot de passe : ")

        # Création de la requête à envoyer au serveur
        requete = {
            "type_message": "requete",
            "type_action": "CREATION_UTILISATEUR",  ################## vérifier le nom
            "identifiant": None,
            "donnee": {
                "Information": {
                    "Nom": nom,
                    "Prenom": prenom,
                    "Email": email,
                    "Mdp": mot_de_passe,
                },
                "Annuaire_contact": [],
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
            print("Utilisateur créé avec succès !")
            print(f"L'identifiant de l'utilisateur est : {reponse['id_client']}")
            return True, reponse["id_client"]
        else:
            message_erreur = interprete_code_erreur(int(reponse["code_erreur"]))
            print(f"Erreur ({reponse['code_erreur']}) : {message_erreur}")
            return False, None
    except Exception as e:
        print(f"Erreur lors de la création de l'utilisateur : {e}")
        return False, None
