from copyreg import pickle
import os
from typing import List, Tuple
import pickle
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

cog_endpoint = os.getenv("COG_SERVICE_ENDPOINT")
cog_key = os.getenv("COG_SERVICE_KEY")


def azure_dict_offre(tuple_list):

    """
    Prend la liste des résumés avec les clés correspondantes, et crée un dictionnaire pour être utiliser dans le module
    recognize entities
    https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/named-entity-recognition/how-to-call
    """

    # création des dictionnaires 
    doc_list = []
    
    for elt in tuple_list:
        
        dict = {"id": elt[0], "text": elt[1][0:1000]}

        doc_list.append(dict)

        # on a au max des chaînes de 1000 caractères

    return(doc_list)




def entities_recognition(summary, language_code) -> List[str]:
    

    credential = AzureKeyCredential(cog_key)
    
    client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)
    

    #summary = summary.replace(u':', u';')
    
    # on ne garde que les 1000 
    doc = [{'id': 0, "text": summary}]

    
    results = client.recognize_entities(documents=doc,language=language_code)
    
    
    #print("sauvegarde pickle")
    #pickle.dump(results, open( "save.p", "wb" ))

    cat = [results[0].entities[i].category for i in range(0, len(results[0].entities))]
    word = [results[0].entities[i].text for i in range(0, len(results[0].entities))]
    
    # normalement on récupère une liste de dictionnaire de clé 'id' et 'text' avec une liste d'entités
    return cat, word
    
    





    
    
