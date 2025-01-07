import socket as s


class Donnee:
    def __init__(self, nom, prenom, identifiant, email, mdp, telephone, adresse, information):
        self.nom = nom  # Nom de l'utilisateur
        self.prenom = prenom  # Prénom de l'utilisateur
        self.identifiant = identifiant  # Identifiant unique
        self.email = email  # Adresse e-mail
        self.mdp = mdp  # Mot de passe
        self.telephone = telephone  # Numéro de téléphone
        self.adresse = adresse  # Adresse postale
        self.information = information  # Liste d'informations supplémentaires

    def __repr__(self):
        return (f"Donnee(nom={self.nom}, prenom={self.prenom}, identifiant={self.identifiant}, "
                f"email={self.email}, mdp={self.mdp}, telephone={self.telephone}, "
                f"adresse={self.adresse}, information={self.information})")


class Requete:
    def __init__(self, type_message, type_action, identifiant, donnee, code_erreur):
        self.type_message = type_message  # Type du message (ex : "Requête")
        self.type_action = type_action  # Action à effectuer (ex : "Recherche", "Création")
        self.identifiant = identifiant  # Identifiant de la requête
        self.donnee = donnee  # Instance de la classe Donnee
        self.code_erreur = code_erreur  # Code d'erreur éventuel ("0" si tout va bien)

    def __repr__(self):
        return (f"Requete(type_message={self.type_message}, type_action={self.type_action}, "
                f"identifiant={self.identifiant}, donnee={self.donnee}, code_erreur={self.code_erreur})")




"""
Fonctionnalité recherche_contact 
Objectif: affiche un menu au client, prends son choix en entree et le retourne
Parametre:
Auteur: Fatoumata Salia Traore 
"""
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
    choix=int(input("Veuillez renseignez votre choix : "))
    return choix


"""
Fonctionnalité recherche_contact 
Objectif: Permet a un utilisateur de rechercher un contact de son annuaire en reseingnant les information du contact (Nom et Prenom)
Parametre: 
    Nom: char 
    Prenom : char
    socket : socket 
Auteur: Fatoumata Salia Traore 
"""
def recherche_contact(Nom, Prenom, socket):
    try:
        # Création du message de requête pour la recherche de contact
        requete = Requete()

        # Envoi de la requête au serveur via le socket
        socket.sendall(str(requete).encode('utf-8'))

        # Réception de la réponse du serveur
        reponse = socket.recv(1024).decode('utf-8')

        # Traitement de la réponse
        if reponse:
            print("Résultat de la recherche :", reponse)
            return reponse
        else:
            print("Aucun contact trouvé.")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche du contact : {e}")
        return None




















#Partie test
if __name__=="__main__":
    q="maman"

    print(q[0])


"""
#Strcuture :

#-fichier client : Contenant tout ce que est relatif au client
    #-Ulils.py : toute les fonction que les client va utiliser pous ses manip
        #-Creation de compte
        #-Recherche contact
        #-Ajout Contact
        #--autre petites fonction utilitaires
    #client.py : connexion au serveur via les socket (en gros cpmme le main du client)
        #-connection via socket #-connection  au compte client
        #-affichage menu avant et apres connection (on pourrai le mettre dans utils)
        #main dans leque on va tout bien afficher avec des appel de focntion de utils 

#-fichier client :
    #-Ulils.py : toute les fonction que les serveur va utiliser pous ses manip
        #-Creation de compte
        #-Recherche contact
        #-Ajout Contact
        #--autre petites fonction utilitaires
    #serveur.py :connexion au serveur via les socket  (en gros cpmme le main du serveur)
        #metre en place le fichier json (remplir au prealable)
        #-connection via socket
        #main dans leque on va tout bien afficher avec des appel de focntion de util

"""