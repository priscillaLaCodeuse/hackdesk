# 📌 HackDesk 🐼

<!-- #### URL : [Visitez HackDesk sur Render](https://hackdesk.onrender.com/) -->

#### Vidéo Demo : [Lien vidéo](https://youtu.be/yfdCKZ1kviA)

#### Description :

HackDesk est une application web conçue comme un **bureau virtuel de gestion de projets pour les développeurs**.

Elle permet à un utilisateur de gérer efficacement ses **clients**, ses **projets** et ses **tâches**, tout en offrant un **tableau de bord clair** pour suivre l’avancement global.

Ce projet a été développé comme **projet final du cours CS50**, et il illustre ma capacité à concevoir une application web complète intégrant : 
- la gestion de la base de données,
- l’authentification des utilisateurs,
- l’envoi d’e-mails,
- et la création d’une interface utilisateur intuitive.

---

## 🌟 Objectifs du projet

Le but de HackDesk est double :  

- **Côté utilisateur** : proposer un outil pratique pour les développeurs web souhaitant suivre ses projets clients dans un espace centralisé. 

- **Côté apprentissage** : mettre en pratique les compétences acquises dans le cadre du CS50, notamment en programmation Python, bases de données relationnelles, et développement web. 

HackDesk se distingue par une organisation claire en trois entités principales : 

- **Clients** → stocker les coordonnées et informations de chaque client, 
- **Projets** → rattacher un projet à un client et à un utilisateur, 
- **Tâches** → subdiviser un projet en tâches mesurables pour suivre le temps et le statut. 

---

## ✨ Fonctionnalités principales

### 🔐 Authentification
- Inscription avec cryptage de mot de passe via **Werkzeug**. 
- Connexion / déconnexion avec gestion de session via **Flask-Login**. 
- Vérification des champs obligatoires et gestion des erreurs utilisateur. 

### 📊 Tableau de bord
- Vue globale du nombre de projets créés, projets en cours, projets terminés et clients enregistrés. 
- Interface simple et claire permettant de visualiser l’avancement. 

### 👥 Gestion des clients
- Ajouter, modifier ou supprimer un client. 
- Stocker les coordonnées (nom, entreprise, adresse, email, téléphone, etc.).  
- Lier les projets aux clients correspondants. 

### 📁 Gestion des projets
- Ajouter un projet avec description, URL, serveur d’hébergement, tarif horaire et statut. 
- Modifier ou supprimer un projet existant. 
- Suivre l’état d’avancement (En cours / Terminé). 

### ✅ Gestion des tâches
- Ajouter des tâches associées à un projet. 
- Suivre le statut (En cours, terminé, etc.) et le temps passé. 
- Modifier ou supprimer des tâches. 

### 📧 Notifications par e-mail
- Envoi automatique d’un e-mail de bienvenue lors de l’inscription. 
- Système extensible pour inclure des notifications liées aux projets ou réinitialisation de mot de passe. 

---

## 🛠️ Technologies utilisées

- **Langage** : Python 3.13 
- **Framework web** : Flask 
- **Base de données** : SQLAlchemy (ORM) 
- **Authentification** : Flask-Login 
- **Mailing** : Flask-Mail 
- **Hashing** : Werkzeug (pour sécuriser les mots de passe) 
- **Templates** : Jinja2 avec HTML/CSS 
- **Autres outils** : Dotenv pour la gestion des variables d’environnement 

---
