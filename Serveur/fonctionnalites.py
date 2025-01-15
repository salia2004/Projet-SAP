import json
import os

"""
Fonctionnalité : CHARGER_ANNUAIRE
Objectif : Charger les données de l'annuaire à partir d'un fichier JSON pour initialiser les informations du serveur
Charge l'annuaire à partir d'un fichier JSON.
    :param fichier: Chemin du fichier JSON à charger.
    :return: Liste représentant l'annuaire.
"""


def charger_annuaire(fichier="annuaire.json"):
    chemin_fichier = os.path.join(
        os.path.dirname(__file__), fichier
    )  # Chemin relatif par rapport au script
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            annuaire = json.load(f)
            print("Annuaire chargé avec succès.")
            return annuaire
    except FileNotFoundError:
        print(f"Fichier non trouvé : {fichier}. Création d'un nouvel annuaire.")
        return []  # Retourne un annuaire vide si le fichier n'existe pas
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")
        return []  # Retourne un annuaire vide en cas d'erreur de lecture


"""
Fonctionnalité : SAUVEGARDER_ANNUAIRE
Objectif : Sauvegarder l'annuaire actuel dans un fichier JSON afin de conserver les données persistantes
  Sauvegarde l'annuaire dans un fichier JSON.
    :param annuaire: Liste représentant l'annuaire.
    :param fichier: Chemin du fichier JSON où sauvegarder l'annuaire.
"""


def sauvegarder_annuaire(annuaire, fichier="annuaire.json"):
    chemin_fichier = os.path.join(os.path.dirname(__file__), fichier)
    try:
        with open(chemin_fichier, "w", encoding="utf-8") as f:
            json.dump(annuaire, f, ensure_ascii=False, indent=4)
            print("Annuaire sauvegardé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'annuaire : {e}")


"""
Fonctionnalité : TRAITER_REQUETE
Objectif : Analyser et traiter une requête reçue du client en fonction de son type (connexion, consultation de contact, etc.)
 Traite une requête reçue d'un client et retourne une réponse appropriée.
    :param data: Données reçues du client (chaîne encodée).
    :param annuaire: L'annuaire contenant les informations des utilisateurs.
    :return: Réponse sous forme de chaîne JSON.
"""


def traiter_requete(data, annuaire):
    import json

    try:
        # Convertir la chaîne reçue en un objet Requete
        requete = json.loads(data)
        if requete["type_action"].upper() == "CONNEXION":
            # Traiter une requête de connexion
            email = requete["donnee"]["email"]
            mdp = requete["donnee"]["mdp"]

            utilisateur = next(
                (user for user in annuaire if user["Information"]["Email"] == email),
                None,
            )
            if not utilisateur:
                return json.dumps(
                    {
                        "type_message": "reponse",
                        "type_action": "CONNEXION",
                        "code_erreur": 409,  # Utilisateur non trouvé
                        "donnee": None,
                    }
                )
            if utilisateur["Information"]["Mdp"] != mdp:
                return json.dumps(
                    {
                        "type_message": "reponse",
                        "type_action": "CONNEXION",
                        "code_erreur": 407,  # Mot de passe incorrect
                        "donnee": None,
                    }
                )

            # Connexion réussie
            return json.dumps(
                {
                    "type_message": "reponse",
                    "type_action": "CONNEXION",
                    "code_erreur": "0",  # Pas d'erreur
                    "donnee": {"id": utilisateur["Id"]},
                } )
        elif requete["type_action"] == "CONSULTER_CONTACT":
            # Traiter une requête de consultation de contact
            id_client = requete["identifiant"]  # id client
            nom = requete["donnee"]["nom"]
            prenom = requete["donnee"]["prenom"]

            utilisateur = next((user for user in annuaire if user["Id"] == id_client), None)
            if not utilisateur:
                return json.dumps(
                    {
                        "type_message": "reponse",
                        "type_action": "CONSULTER_CONTACT",
                        "code_erreur": 409,  # Utilisateur non trouvé
                        "donnee": None,
                    }
                )
            print(utilisateur["Annuaire_contact"])
            contact = []
            for c in utilisateur["Annuaire_contact"] :
                if c["Nom"].strip().lower() == nom.strip().lower() and c["Prenom"].strip().lower() == prenom.strip().lower():
                    contact.append(c)
            if not contact:
                return json.dumps(
                    {
                        "type_message": "reponse",
                        "type_action": "CONSULTER_CONTACT",
                        "code_erreur": 404,  # Contact non trouvé
                        "donnee": None,
                    })
            # Contact trouvé
            return json.dumps(
                {
                    "type_message": "reponse",
                    "type_action": "CONSULTER_CONTACT",
                    "code_erreur": "0",  # Pas d'erreur
                    "donnee": contact,
                }
            )

        elif requete["type_action"].upper() == "CREATION_COMPTE":
            # Traiter une requête de création utilisateur
            informations_utilisateur = requete.get("donnee")

            if not informations_utilisateur or not all(
                key in informations_utilisateur
                for key in ["email", "mdp", "nom", "prenom"]
            ):
                return json.dumps(
                    {
                        "type_message": "reponse",
                        "type_action": "CREATION_COMPTE",
                        "code_erreur": 400,  # Requête mal formulée (champs manquants)
                        "donnee": None,
                    }
                )
            email = informations_utilisateur["email"]
            mdp = informations_utilisateur["mdp"]
            nom = informations_utilisateur["nom"]
            prenom = informations_utilisateur["prenom"]
            # Si l'utilisateur existe déjà
            if any(user for user in annuaire if user["Information"]["Email"] == email):
                return json.dumps(
                    {
                        "type_message": "reponse",
                        "type_action": "CREATION_COMPTE",
                        "code_erreur": 405,  # Compte déjà existant
                        "donnee": None,
                    }
                )
            # Si l'utilisateur n'existe pas déjà, le créer
            nouvel_utilisateur = {
                "Id": len(annuaire) + 1,
                "Information": {
                    "Email": email,
                    "Mdp": mdp,
                    "Nom": nom,
                    "Prenom": prenom,
                },
                "Utilisateurs_autorise": [],  # La liste des utilisateurs autorisé à la lecture est vide au début
                "Annuaire_contact": [],  # L'annuaire de contacts de l'utilisateur est vide au début
            }
            annuaire.append(nouvel_utilisateur)
            sauvegarder_annuaire(annuaire)
            # utilisateur créé
            return json.dumps(
                {
                    "type_message": "reponse",
                    "type_action": "CREATION_COMPTE",
                    "code_erreur": "0",  # Pas d'erreur
                    "donnee": {"id_client": nouvel_utilisateur["Id"]},
                }
            )
        elif requete["type_action"].upper() == "AJOUT_CONTACT":
            # Traiter une requête d'ajout de contact
            return json.dumps(ajouter_contact(requete, annuaire))
        
        elif requete["type_action"].upper() == "DECONNEXION":
            print(f"Déconnexion demandée par le client {requete['identifiant']}")
            return json.dumps({
                "type_message": "reponse",
                "type_action": "DECONNEXION",
                "code_erreur": "0",  # Pas d'erreur
                "donnee": None,
            })

        else:
            # Si l'action n'est pas reconnue
            return json.dumps({
                    "type_message": "reponse",
                    "type_action": requete["type_action"],
                    "code_erreur": 400,  # Requête mal formulée
                    "donnee": None,
                })

    except Exception as e:
        print(f"Erreur lors du traitement de la requête : {e}")
        return json.dumps(
            {
                "type_message": "reponse",
                "type_action": "ERREUR",
                "code_erreur": 400,  # Requête mal formulée
                "donnee": None,
            }
        )


"""
Fonctionnalité : AJOUT_CONTACT
Objectif : Ajouter un nouveau contact dans l'annuaire d'un utilisateur spécifique.
Auteur : [MAIGA Aminata Alidji]
"""

def ajouter_contact(data, annuaire):
    """
    Ajoute un contact à l'annuaire d'un utilisateur.

    :param data: Requête contenant les informations du contact à ajouter.
    :param annuaire: Liste représentant l'annuaire complet.
    :return: Réponse sous forme de dictionnaire.
    """
    # Extraire les données de la requête
    id_utilisateur = data.get("identifiant")
    contact = data.get("donnee")

    # Vérifier si l'utilisateur existe dans l'annuaire
    utilisateur = next(
        (user for user in annuaire if user["Id"] == id_utilisateur), None
    )
    if not utilisateur:
        return {
            "type_message": "reponse",
            "type_action": "AJOUT_CONTACT",
            "code_erreur": 409,  # Utilisateur non trouvé
            "donnee": None,
        }

    # Vérifier si le contact existe déjà dans l'annuaire de l'utilisateur
    for c in utilisateur["Annuaire_contact"]:
        if c["Email"] == contact["email"]:
            return {
                "type_message": "reponse",
                "type_action": "AJOUT_CONTACT",
                "code_erreur": 403,  # Contact déjà présent
                "donnee": None,
            }

    # Ajouter le contact à l'annuaire
    utilisateur["Annuaire_contact"].append(contact)

    # Sauvegarder les modifications dans le fichier JSON
    sauvegarder_annuaire(annuaire)

    return {
        "type_message": "reponse",
        "type_action": "AJOUT_CONTACT",
        "code_erreur": "0",  # Pas d'erreur
        "donnee": contact,
    }
