# Projet 2 - Groupe 3

Membres du groupe: Cynthia, William, Gabriel

## Configuration préalable

* Placé vous dans l'environnement virtuel qui est founit dans le répertoire:

```bash
pipenv shell
```

* Pour créer la base de données qui sera exploitée dans l'application web, le module pipeline.py appel d'autres modules qui exploitent la librairie spacy. Vous devrez donc installer le dictionnaire suivant pour spacy. A l'extérieur de votre environnement virtuel, exécutez:

```bash
pipenv run python3 -m spacy download fr_core_news_lg
```

* L'étape d'enrichissement fait appel aux fonctionnalités d'Azure Cognitive service. Vous devrez donc vous procurez un identifiant et une clé Azure que vous renseignerez dans un fichier .env dans le même répertoire que le module pipeline.py:

```bash
COG_SERVICE_ENDPOINT=
COG_SERVICE_KEY= 
```
Attention! Ne communiquez jamais vos identifiants et votre clé, c'est pourquoi le fichier doit être un fichier caché que vous incluerait dans votre fichier .gitignore.

## Utilisation du module pipeline.py

Le module pipeline.py lance le pipeline d'extraction, du chargement, d'enrichissement de données afin d'être exploitée dans notre application job_app suivant le [schéma](../docs/PipelineProjet2-Groupe3.jpg) du pipeline.

Le module pipeline.py s'articule autour des [étapes](../docs/database_projet_2.jpg) suivantes:  
1. Scrapping du site Pôle Emploi sur l'ensemble des pages résultantes de la recherche "Développeur en intelligence artificielle".
2. Copie des données scrappées dans la table temporaire "raw_data". Seules les données nouvelles seront copiées dans la table clean_data.
3. Les données sont réparties dans les tables du modèle analytiques.
4. La table centrale "offre" est enrichie par un résumé s'appuyant sur la librairie spacy.
5. La table "motcle" est remplie en faisant appel au SDK TextAnalytics de la suite Azure qui détecte les entités importantes dans le résumé et les catégorisent.

Le module pipeline.py générera ou mettra à jour la base de données qui sera exploitée par l'application web.

## Utilisation de l'application web


Vous pouvez tester l'application en local et en mode développeur. Placez-vous dans l'environnement virtuel dédié et éxecutez la commande suivante:

```bash
pipenv shell
```

```bash
python3 app.py runserver
```

Pour aller plus loin dans l'utilisation de l'application, vous pouvez vous référer au [tutoriel dédié](../docs/Guide_utilisateur_OpenAI.pdf)

## Bibliographie

[Réaliser un résumé d'un texte avec la librairie spacy](https://www.numpyninja.com/post/text-summarization-through-use-of-spacy-library#:~:text=Steps%20to%20Text%20Summarization%3A&text=Now%20lets%20see%20how%20to,library%20%2C%20also%20import%20stop%20words.&text=Import%20punctuation%20marks%20from%20string,next%20line%20tag%20in%20it.&text=Store%20a%20text%20in%20variable,need%20to%20summarise%20the%20text.)

[Système de recommandation](https://larevueia.fr/le-machine-learning-pour-les-systemes-de-recommandations/)  
[Les algorithmes de recommandation](https://blog.octo.com/introduction-aux-algorithmes-de-recommandation-lexemple-des-articles-du-blog-octo/)  
[Documentation sur le Named Entity Recognition de l'API Azure](https://docs.microsoft.com/en-us/python/api/azure-ai-textanalytics/azure.ai.textanalytics.textanalyticsclient?view=azure-python#detect-language-documents----kwargs-)  
[Documentation sur le Named Entity Recognition du SDK Azure](https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/named-entity-recognition/overview)  
[Réaliser le  Named Entity Recognition avec scikit-learn](https://towardsdatascience.com/named-entity-recognition-and-classification-with-scikit-learn-f05)

