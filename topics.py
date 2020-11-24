from gensim.models import LdaModel
from gensim import corpora

def get_topics(chapters, nb_topics=10, nb_words=10):
    
    chapters_token = [[line.split(' ') for line in c] for c in chapters]
    
    dictionary = [corpora.Dictionary(c) for c in chapters_token]

    corpus_chapters = [[dictionary[i].doc2bow(token) for token in c] for i, c in enumerate(chapters_token)]

    lda_chapters = [LdaModel(corpus_c, num_topics=nb_topics, passes=3) for corpus_c in corpus_chapters]

    topics = list()
    for i, lda_c in enumerate(lda_chapters):
        topics.append([])
        for j in range(nb_topics):
            words = []
            # On regarde les 10 mots les plus associés au topic
            for x in lda_c.show_topic(j, topn=nb_words):
                words.append(dictionary[i][int(x[0])])
                
            #print(words)
            topics[i].append(words)

    
    return topics