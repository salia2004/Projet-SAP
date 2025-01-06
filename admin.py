import json


def creation_compte():
    email = input("saisir l'adresse mail :\n")
    nom = input("Saisir le nom :\n")
    prenom = input("Saisir le prénom : \n")
    mot_de_passe = input("Saisir le mot de passe : \n")

    if not nom or not prenom or not email:
        return {"code_erreur": 402}
    with open("utilisateurs.json", "r") as json_file:
        utilisateurs = json.load(json_file)

    for id_utilisateur, donnees_utilisateur in utilisateurs["utilisateurs"].items():
        if donnees_utilisateur["email"] == email:
            return {"code_erreur": 403}
    id = str(len(utilisateurs["utilisateurs"]) + 1)
    utilisateurs["utilisateurs"][id] = {
        "nom": nom,
        "prenom": prenom,
        "email": email,
        "contacts": [],
    }

    with open("utilisateurs.json", "w") as json_file:
        json.dump(utilisateurs, json_file, indent=4)
    return {"code_erreur": 0, "id": id}


result = creation_compte()
print(result)
