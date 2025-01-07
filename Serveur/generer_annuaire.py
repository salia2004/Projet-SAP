#Ce programe sert a initaliser l'annnuaire au prea

import random
import string
import json

# Fonction pour générer un mot de passe aléatoire
def generer_mdp(longueur=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    mdp = ''.join(random.choice(caracteres) for _ in range(longueur))
    return mdp

# Fonction pour générer un numéro de téléphone aléatoire
def generer_numero_telephone():
    return f"06{random.randint(10000000, 99999999)}"

# Fonction pour générer une adresse postale aléatoire
def generer_adresse_postale():
    numero = random.randint(1, 200)
    rue = random.choice(["rue de Paris", "avenue de Lyon", "boulevard Saint-Michel", "place du Capitole", "chemin des Écoliers","chemind de dardagna"])
    ville = random.choice(["Paris", "Lyon", "Marseille", "Toulouse", "Nice","Bordeaux","Lille"])
    code_postal = random.randint(10000, 99999)
    return f"{numero} {rue}, {ville}, {code_postal}"

# Fonction principale pour générer le fichier JSON
def generer_json():
    prenoms = ["Kevin", "Abdel", "Balla", "Sarah", "Yves","Aminata","Fatoumata","Amina"] * 20  
    noms = ["Dupont", "Dubois", "Traore", "Bonneau", "Konaté","Didiane"] * 20 

    utilisateurs = []

    for i in range(2, 102):
        nom = random.choice(noms)
        prenom = random.choice(prenoms)
        email = f"{nom.lower()}.{prenom.lower()}@annuaire.com"
        telephone = generer_numero_telephone()
        adresse = generer_adresse_postale()
        mdp = generer_mdp()

        utilisateur = {
            "Id": i,
            "Information": {
                "Nom": nom,
                "Prenom": prenom,
                "Email": email,
                "Adresse postale": adresse,
                "Numéro de téléphone": telephone,
                "Mdp": mdp
            },
            "Utilisateurs_autorise": [],
            "Annuaire_contact": [
                {
                    "Nom": random.choice(noms),
                    "Prenom": random.choice(prenoms),
                    "Email": f"{random.choice(noms).lower()}.{random.choice(prenoms).lower()}@contact.com",
                    "Adresse postale": generer_adresse_postale(),
                    "Numéro de téléphone": generer_numero_telephone()
                } for _ in range(random.randint(0, 10))  # Chaque utilisateur a entre 5 et 10 contacts
            ]
        }
        utilisateurs.append(utilisateur)

    # Sauvegarde dans un fichier JSON
    with open("annuaire.json", "w", encoding="utf-8") as fichier:
        json.dump(utilisateurs, fichier, ensure_ascii=False, indent=4)

    print("Fichier JSON 'annuaire.json' généré avec succès.")

if __name__=="__main__":
    generer_json()