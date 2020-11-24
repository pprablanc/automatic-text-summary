import spacy
import nltk
from nltk.corpus import stopwords

import pandas as pd

import matplotlib.pyplot as plt

from collections import defaultdict


"""
Renvoie une liste par chapitre contenant les entités et leur nombre d'occurences.
"""
def get_named_entities(chapters):
    stop = set(stopwords.words('english'))
    stop.add('shall')
    stop.add('said')
    stop.add('ah')
    stop.add('oh')
    stop.add('ahah')
    stop.add('h')
    stop.add('s')

    # Modèle de langage utilisé par les différentes foncitons (anglais)
    # Requiert "python -m spacy download xx_ent_wiki_sm"
    model = 'en_core_web_sm'
    # Requiert "python -m spacy download en_core_web_sm"
    # self.model = 'xx_ent_wiki_sm'
    nlp = spacy.load(model)

    docs = [nlp(' '.join(chapter)) for chapter in chapters]

    entities_list = []

    for doc in docs:                
        # On les met dans un tableau et on compte les occurences
        entities = []
        for ent in doc.ents:
            if (ent.label_ == "GPE" or 
                ent.label_ == "LOC" or 
                ent.label_ == "PERSON" or 
                ent.label_ == "ORG" or 
                ent.label_ == "NORP"):
                
                # On enlève les stopwords dans les noms
                tmp = ' '.join([word for word in ent.text.split() if word.lower() not in stop])
                
                # On supprime les entités vide et les espaces sur les bords
                tmp = tmp.strip()
                if tmp:
                    entities.append(tmp)

        # Liste d'entités uniques
        entities_list.append(list(set(entities)))

    return entities_list



def filter_entities(entities_list):
    # On compte le nombre de fois qu'une entité apparait
    entities_occurences = defaultdict(int)
    for k in range(len(entities_list)):
        for entity in entities_list[k]:
            entities_occurences[entity.lower()] += 1


    for k in range(len(entities_list)):
        to_remove = []
        for j in range(len(entities_list[k])):
            # On evite les apax
            if entities_occurences[entities_list[k][j].lower()] < 2:
                to_remove.append(entities_list[k][j])
                continue
                
            for i in range(j+1, len(entities_list[k])):
                # On evite les apax
                if entities_occurences[entities_list[k][i].lower()] < 3:
                    to_remove.append(entities_list[k][i])
                    continue
                    
                # Si une entité en contient une autre
                if (entities_list[k][j].find(entities_list[k][i]) != -1 or 
                    entities_list[k][i].find(entities_list[k][j]) != -1):
                    
                    # On ne garde que la plus fréquente des deux
                    if entities_occurences[entities_list[k][j].lower()] > entities_occurences[entities_list[k][i].lower()]:
                        to_remove.append(entities_list[k][i])
                    else:
                        to_remove.append(entities_list[k][j])
            
        to_remove = list(set(to_remove))
        print('Entities of chapter ', k)
        print(to_remove)
        print()
        print(entities_list[k])
        print()
        [entities_list[k].remove(word) for word in to_remove]
        print(entities_list[k])
        print()

    return entities_list