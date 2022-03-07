import spacy
import string
from spacy.lang.fr.stop_words import STOP_WORDS
from heapq import nlargest
from string import punctuation

# https://www.numpyninja.com/post/text-summarization-through-use-of-spacy-library#:~:text=Steps%20to%20Text%20Summarization%3A&text=Now%20lets%20see%20how%20to,library%20%2C%20also%20import%20stop%20words.&text=Import%20punctuation%20marks%20from%20string,next%20line%20tag%20in%20it.&text=Store%20a%20text%20in%20variable,need%20to%20summarise%20the%20text.


punctuation=punctuation+ '\n'

# on récupère les mots de liaison en Français
stopwords=list(STOP_WORDS)

def summarize_from_description(text):
    
    # traitement préalable du texte des descriptions
    # on ne traite que les éléments qui ne sont pas essentiels
    # à la structuration d'une phrase
    text = text.replace(u'\xa0', u' ')
    text = text.replace(u'&nbsp',u' ')
    text = text.replace(u'&amp;',u'&')
    #text = text.replace(u',',u' ')
    text = text.replace(u'-',u'')
    #text = text.replace(u';',u' ')
    #text = text.replace(u'.', u' ')
    #text = text.replace(u'...', u' ')
    #text = text.replace(u'/', u'')
    #text = text.replace(u':', u';')
    text = text.replace(u'*', u'')
    text = text.replace(u'\n', u' ')
    #text = text.replace(u'\t', u' ')
    #text = text.replace(u'    ', u' ')
    #text = text.replace(u'  ', u' ')
    # Il reste encore des doubles espaces en fin de lignes
    #text = text.replace(u'  ', u' ')

    # dictionnaire long spécialisé "informations"
    nlp = spacy.load("fr_core_news_lg")
   
    doc = nlp(text)
    
    word_frequencies={}

    for word in doc:
        
        # on calcule l'occurence de chaque mot sans tenir compte 
        # des caractères de ponctuation et des mots de liaison en Français
        # les mots sont passés en minuscule

        if word.text.lower() not in stopwords:
            
            if word.text.lower() not in punctuation:

                # on crée un dictionnaire avec comme clé le mot
                # et son occurence

                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    # on récupère l'occurence la plus grande tout mot confondu
    max_frequency=max(word_frequencies.values())

    # on normalise la fréquence de chaque mot par rapport à l'occurence maximale
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency

    # on crée la liste des phrases dans le text
    sentence_tokens= [sent for sent in doc.sents]

    # on donne un score à chaque phrase
    sentence_scores = {}

    for sent in sentence_tokens:

        for word in sent:
            
            if word.text.lower() in word_frequencies.keys():

                # on augmente le score de chaque phrase avec l'occurence normalisée
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]

    # on ne garde que 25% du total des phrases avec les mots qui reviennent le plus souvent
    select_length=int(len(sentence_tokens)*0.25)

    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)

    # on assemble les phrases restantes pour constituer le résumé final
    final_summary=[word.text for word in summary]

    summary=''.join(final_summary)


    return(summary)

