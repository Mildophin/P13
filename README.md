# Projet 13 du parcours python d'OC : ORANGE COUNTY LETTINGS

## Description

Orange County Lettings (OC Lettings) est une start-up fictive spécialisée dans la location de biens immobiliers.

Ce projet consiste à refactorer le code de l'application du site web d'OC Lettings et à le déployer sur Heroku en utilisant un conteneur et un pipeline CI/CD. Le site web reflétant le résultat du refactoring et du déploiement est disponible à l'adresse suivante :

https://oclettings-heroku1.herokuapp.com/

Ce projet a été réalisé dans le cadre du parcours python d'OC.

Un push a été ajouté pour la présentation.

## Contexte technique

Le projet utilise les technologies suivantes :

* [Python](https://www.python.org) comme langage de programmation
* [Django](https://www.djangoproject.com/) en tant que framework web
* [Pytest](https://pytest.org) and [Coverage](https://pypi.org/project/coverage/) pour les tests
* [Docker](https://www.docker.com) pour la conteneurisation
* [CircleCI](https://www.circleci.com) pour l'intégration continue
* [Heroku](https://www.heroku.com) pour le déploiement
* [Sentry](https://www.sentry.io) pour le monitoring

## Déploiement local

**Python 3** est nécessaire pour faire fonctionner le site web.

1. Clonez ce dépôt (ou téléchargez le code [sous forme de fichier zip](https://github.com/Mildophin/P13/archive/refs/heads/master.zip)), accédez au dossier racine du dépôt, créez et activez un environnement virtuel, installez les dépendances du projet :

```
git clone https://github.com/Mildophin/P13.git
cd P13
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

2. Exécuter le serveur

```
$ python manage.py runserver
```

## Utilisation

Le site web est disponible à l'adresse suivante :

```
http://localhost:8000/
```

## Administration

L'application est fournie avec un site d'administration.

```
http://localhost:8000/admin/
```

Seuls les utilisateurs ayant le statut `superuser` peuvent se connecter au site d'administration.

La base de données est fournie avec un compte superutilisateur préconfiguré :

utilisateur: `admin`

mot de passe: `Heroku123!`

## Tests

La suite de tests peut être exécutée à l'aide de la commande suivante :

```
pytest
```

Le rapport de couverture peut être généré à l'aide de la commande suivante :

```
coverage run -m pytest
```

Le rapport html peut être généré avec la commande suivante :

```
coverage html
```

Le rapport sera créé dans le sous-dossier `htmlcov/`.

## Déploiement local à l'aide de Docker CLI

Le dépôt contient un `Dockerfile`qui permet de construire facilement un conteneur Docker et d'exécuter localement l'application. Le même conteneur peut être utilisé pour le déploiement en production.

1. Télécharger et installer [Docker engine](https://docs.docker.com/engine/install/) selon les exigences de votre système.

2. Naviguez vers le dossier racine de l'application et construisez le conteneur nommé `oclettings-docker` :

```
docker build --platform linux/amd64 -t oclettings-docker .
```

3. Exécuter le conteneur localement:

```
docker run --platform linux/amd64 -e DJANGO_SETTINGS_MODULE=config.settings.local -e PORT=8000 -p 127.0.0.1:8000:8000 -d oclettings-docker:latest
```

Le site web est désormais accessible localement à partir d'un navigateur web à l'adresse suivante `http://127.0.0.1:8000`

## Déploiement à l'aide de Heroku CLI

L'application est pré-configurée pour être déployée sur Heroku pour la production. Cette procédure suppose que vous avez déjà créé localement un conteneur nommé `oclettings-docker` comme décrit ci-dessus.

1. Créez un compte utilisateur sur [Heroku](https://www.heroku.com)
2. Télécharger et installer [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
3. Connectez-vous et créez une nouvelle application Heroku (remplacer `<app_name>` avec le nom d'application que vous avez choisit)

```
heroku login
```

```
heroku apps:create <app_name>
```

4. Configurer la clé secrète de Django comme une variable d'environnement (remplacez `<your_secret_key>` par votre clé secrète).

```
heroku config:set DJANGO_SECRET_KEY='<your_secret_key>' -a <app_name>
```

5. Retaguer le conteneur en fonction du nom de l'application Heroku.:

```
docker tag oclettings-docker:latest registry.heroku.com/<app_name>/web:latest
```

6. Poussez le conteneur et libérez l'application:

Connectez-vous au registre des conteneurs Heroku:

```
heroku container:login
```

'Push' le conteneur et lancer l'application :
```
docker push registry.heroku.com/<app_name>/web:latest
heroku container:release web -a <app_name>
```

7. Vous pouvez maintenant consulter le site web à l'adresse suivante: `https://<app_name>.herokuapp.com`.

## Déploiement à l'aide de CircleCI CI/CD Pipeline

Le pipeline créé pour le projet est disponible à l'adresse suivante : <https://app.circleci.com/pipelines/github/Mildophin/P13>.

Le conteneur du dépôt contient un fichier de configuration pour CircleCI : `.circleci/config.yml`. Fichier qui importe le *workflow* nécessaire à l'application:

* build:
  * construit une image de conteneur docker incorporant Python 3.9 basée sur les [Images de l'héritage linguistique de CircleCi](https://circleci.com/docs/2.0/circleci-images/#legacy-language-images)
  * crée un environnement virtuel, installe les paquets tiers nécessaires au projet
  * sauvegarde l'environnement dans le cache
* test:
  * construit l'image docker CircleCI Python 3.9 et restaure l'environnement à partir du cache
  * exécute la suite de tests en utilisant la commande `pytest`
  * les tests ne commencent **qu'après que la construction du travail ait fonctionné**.
* linting:
  * construit l'image docker CircleCI Python 3.9 et restaure l'environnement à partir du cache
  * exécute le contrôle de qualité en utilisant la commande `flake8`.
  * le linting commence seulement **après que le job build soit terminé avec succès**.
* package:
  * construit l'image docker CircleCI Python 3.9 et restaure l'environnement à partir du cache
  * construit un conteneur Docker selon les exigences du fichier `Dockerfile`
  * push le conteneur Docker vers le Dockerhub
  * le travail sur le package commence seulement **après que les travaux de test et de linting soient terminés avec succès**
* deploy:
  * pull le conteneur Docker précédemment construit depuis le Dockerhub
  * tague le conteneur Docker comme il se doit pour push le conteneur vers le registre de conteneurs Heroku.
  * push le conteneur Docker au registre de conteneurs Heroku
  * lance l'application Heroku
  * le travail de déploiement ne démarre qu'une fois que le travail de déploiement est terminé avec succès**

Les tâches *build, test, linting* sont exécutées automatiquement chaque fois qu'un nouveau commit est poussé vers le dépôt Github.

Les *jobs package, deploy* sont exécutés automatiquement chaque fois qu'un **nouveau commit de la branche main** est poussé vers le dépôt Github.

## L'environnement CircleCI

L'environnement du projet CircleCI comprend les variables suivantes :

`DOCKER_USER`: le nom d'utilisateur du Dockerhub où est push le conteneur construit par CircleCI

`DOCKER_ACCESS_TOKEN`: le jeton d'accès correspondant au nom d'utilisateur ([utilisation des jetons d'accès](https://docs.docker.com/docker-hub/access-tokens/) est recommandé au lieu du mot de passe)

`HEROKU_APP_NAME`: le nom de l'application Heroku

`HEROKU_API_KEY`: la clé API correspondant au compte Heroku

Ces variables sont créées en tant que [variables d'environnement pour le projet](https://circleci.com/docs/2.0/env-vars/#setting-an-environment-variable-in-a-project) pour exécuter la pipeline sur un dépôt CircleCI différent, et modifié si nécessaire pour utiliser un compte ou un nom d'application Docker ou Heroku différent.

## Monitoring avec Sentry

Un processus de surveillance simple est mis en place. La navigation vers la page `/sentry-debug` va lever une erreur de serveur qui sera capturée comme un problème dans un projet Sentry.

Le nom de la source de données (DSN) du projet doit être stocké dans la variable d'environnement SENTRY_DSN dans Heroku (remplacez <your_DSN> par le DSN de votre projet et <app_name> par le nom de l'application Heroku) :

```
heroku config:set SENTRY_DSN='<your_DSN>' -a <app_name>
```

Le rapport sur les erreurs de Sentry est disponible à l'adresse suivante :
<https://sentry.io/share/issue/53baf13da5db4ff1a52f9c0b6c91dacb/>
