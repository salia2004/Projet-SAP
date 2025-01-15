# Projet : Service d’Annuaire Partagé

<<<<<<< HEAD
## Description du Projet
Ce projet consiste à développer une application distribuée basée sur une architecture client-serveur pour 
la gestion d’annuaires partagés. Chaque utilisateur dispose d’un compte utilisateur lié à son propre 
annuaire personnel. L’administrateur du serveur est chargé de gérer les comptes utilisateurs, tandis que 
les utilisateurs peuvent ajouter, modifier, supprimer, et rechercher des contacts. Le projet est développé 
en Python et les données sont stockées dans des fichiers JSON.

## Fonctionnalités Implémentées
### Côté Serveur :
1. Gestion des comptes utilisateurs (création, modification, suppression).
2. Gestion des annuaires personnels et partagés.
3. Autorisation de consultation pour des annuaires tiers.
4. Réponses aux requêtes clients via des sockets.

### Côté Client :
1. Connexion et authentification.
2. Gestion des contacts dans l’annuaire (ajout, modification, suppression, recherche).
3. Consultation d’annuaires tiers avec autorisations.
4. Déconnexion sécurisée.

## Organisation des Fichiers
### Répertoires Principaux
- `Client/`
  - `client.py` : Fichier principal pour la gestion des interactions client.
  - `Fonctionnalite.py` : Fonctions utilitaires pour la gestion des contacts et des comptes.
- `Serveur/`
    - `serveur.py` : Serveur principal pour la gestion des requêtes des clients.
    - `generer_annuaire.py` : Script pour initialiser les données des annuaires en JSON.
    - Fichiers JSON :
        - `annuaire.json` : Contient les informations des contacts pour chaque utilisateur.
- Admin.py : La fonction creation_compte dans le fichier administrateur.py permet à un administrateur de 
créer un compte utilisateur. Les informations sont enregistrées dans le fichier JSON utilisateurs.json. 
Cette fonctionnalité inclut des vérifications pour garantir l'unicité de l'adresse email et la validité des 
données saisies.

## Instructions pour l’Exécution
1. **Démarrage du serveur** :
   - Exécuter le script serveur.py.
2. **Lancement du client** :
   - Exécuter le script client.py.
   - Suivre le menu pour se connecter et gérer les contacts.

## Répartition des Tâches principales
- **Création de Compte et Gestion Utilisateur** : [ DIDANE Amina]
- **Ajout de Contact** : [MAIGA Aminata Alidji]
- **Recherche de Contact et Conclusion** : [ TRAORE Fatoumata Salia]
