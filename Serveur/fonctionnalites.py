import json

"""
Fonctionnalité : CHARGER_ANNUAIRE
Objectif : Charger les données de l'annuaire à partir d'un fichier JSON pour initialiser les informations du serveur
Charge l'annuaire à partir d'un fichier JSON.
    :param fichier: Chemin du fichier JSON à charger.
    :return: Liste représentant l'annuaire.
"""
def charger_annuaire(fichier="annuaire.json"):
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
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
    try:
        with open(fichier, 'w', encoding='utf-8') as f:
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

        if requete['type_action'].upper() == "CONNEXION":
            # Traiter une requête de connexion
            email = requete['donnee']['email']
            mdp = requete['donnee']['mdp']
            
            utilisateur = next((user for user in annuaire if user['Information']['Email'] == email ), None)

            if not utilisateur:
                return json.dumps({
                    "type_message": "reponse",
                    "type_action": "CONNEXION",
                    "code_erreur": 409,  # Utilisateur non trouvé
                    "donnee": None
                })
            if utilisateur['Information']['Mdp'] != mdp:
                return json.dumps({
                    "type_message": "reponse",
                    "type_action": "CONNEXION",
                    "code_erreur": 407,  # Mot de passe incorrect
                    "donnee": None
                })

            # Connexion réussie
            return json.dumps({
                "type_message": "reponse",
                "type_action": "CONNEXION",
                "code_erreur": "0",  # Pas d'erreur
                "donnee": {"id": utilisateur['Id']}
            })

        elif requete['type_action'].upper() == "CONSULTER_CONTACT":
            # Traiter une requête de consultation de contact
            id_client = requete['identifiant'] #id client 
            nom = requete['donnee']['nom']
            prenom = requete['donnee']['prenom']

            utilisateur = next((user for user in annuaire if user['Id'] == id_client), None)

            if not utilisateur:
                return json.dumps({
                    "type_message": "reponse",
                    "type_action": "CONSULTER_CONTACT",
                    "code_erreur": 409,  # Utilisateur non trouvé
                    "donnee": None
                })

            contact = next(
                (c for c in utilisateur['Annuaire_contact'] if c['Nom'] == nom and c['Prenom'] == prenom),
                None
            )

            if not contact:
                return json.dumps({
                    "type_message": "reponse",
                    "type_action": "CONSULTER_CONTACT",
                    "code_erreur": 404,  # Contact non trouvé
                    "donnee": None
                })

            # Contact trouvé
            return json.dumps({
                "type_message": "reponse",
                "type_action": "CONSULTER_CONTACT",
                "code_erreur": "0",  # Pas d'erreur
                "donnee": contact
            })
        
        elif requete['type_action'].upper() == "CREATION_COMPTE":
            #TRAITEMENT AMINA
            return None
        
        elif requete['type_action'].upper() == "AJOUT_CONTACT":
            #TRAITEMENT AMMINATA
            return None
        #Maybe faire un dernier elif porules autre cas et dire genre focnitonnaliter indissponible 

        # Si l'action n'est pas reconnue
        return json.dumps({
            "type_message": "reponse",
            "type_action": requete['type_action'],
            "code_erreur": 400,  # Requête mal formulée
            "donnee": None
        })

    except Exception as e:
        print(f"Erreur lors du traitement de la requête : {e}")
        return json.dumps({
            "type_message": "reponse",
            "type_action": "ERREUR",
            "code_erreur": 400,  # Requête mal formulée
            "donnee": None
        })