import re

from nltk.corpus import stopwords

def load_corpus():
    dune = open('./Frank Herbert - Dune.txt', encoding = 'latin-1')
    
    lines = dune.read()

    # On sépare en chapitre
    chapters = lines.split('= = = = = =')

    # Les chapitres en lignes
    chapters = [c.split('\n') for c in chapters]

    return chapters


def preprocess(chapters):
    # On enlève les characteres spéciaux
    processed_chapters = [[re.sub(r'[^A-z ]+', ' ', line) for line in c] for c in chapters]
    #chapters = [[re.sub(r'[\n]+', ' ', line) for line in c] for c in chapters]
    #chapters = [[re.sub(r'[^\w\s]+', ' ', line) for line in c] for c in chapters]
    processed_chapters = [[re.sub(r' +', ' ', line)  for line in c] for c in processed_chapters]

    # Stopwords
    # chapters = [[line.split() for line in chapter] for chapter in chapters]
    # chapters = [[' '.join([word for word in line if word.lower() not in stop]) for line in chapter] for chapter in chapters]

    # On enlève les chapitres trop petits
    #chapters = [[line for line in c if len(line) > 20] for c in chapters]
    #chapters = [[line for line in c] for c in chapters if len(c) != 0]
    
    return processed_chapters