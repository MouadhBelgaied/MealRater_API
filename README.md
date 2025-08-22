# Meal Rater API

API REST développée avec **Django REST Framework (DRF)** permettant aux utilisateurs de gérer des repas (**Meal**) et d’attribuer des notes (**Rating**).  
Elle inclut l’authentification via **Token** et une documentation interactive grâce à **Swagger**.

---

## Qu’est-ce qu’une API ?  

Une **API** (Application Programming Interface) agit comme un **serveur dans un restaurant** :  

- **Le client** fait une commande ( = l’utilisateur qui fait une requête)  
- **Le serveur** prend la commande puis revient avec le plat convenable ( = l’API qui communique entre les deux) 
- **Le chef** prépare le plat ( = l'application qui retourne une réponse)   

👉 En résumé, l’API est le **pont** entre un utilisateur et une application.  

<p align="center">
  <img src="https://voyager.postman.com/illustration/diagram-what-is-an-api-postman-illustration.svg" width="600">
</p>

---

## 🛠️ Django REST Framework (DRF)  

**Django REST Framework (DRF)** est une puissante extension de **DJANGO** qui permet de créer facilement des **API RESTful**.  
Il fournit des outils pour :  

- **Sérialiser et désérialiser** les données (JSON <-> Python)  
- Gérer **les permissions et l’authentification**
- Créer rapidement des ***endpoints*** CRUD  

<p align="center">
  <img src="https://www.django-rest-framework.org/img/logo.png" width="300">
</p>

---

## Swagger  

**Swagger** est un outil qui génère automatiquement une **documentation interactive** pour ton **API**.  
Il permet de :  

- **Visualiser** les endpoints disponibles  
- **Tester** les requêtes directement depuis une interface web  
- **Comprendre** rapidement les paramètres et les réponses  

<p align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1400/1*kiRZQkovNoVCTAW4rB7oVQ.png" width="600">
</p>

---

## Fonctionnalités

- Inscription / Connexion / Déconnexion (avec Token d’authentification Auth)
- CRUD User, Meal, Rating (avec permissions)
- Un utilisateur peut créer ou mettre à jour sa note pour un repas
- Calcul automatique de la **moyenne des notes** et du **nombre total de votes** pour chaque repas

---

## Architecture Django

<p align="center">
  <img src="https://miro.medium.com/1*UTCLKbdQmnyywpPqa6aNkw.png" width="600">
</p>

