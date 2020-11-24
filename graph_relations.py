import networkx as nx

import pandas as pd

import matplotlib.pyplot as plt


def draw_entities_relation(entity_matrix, topics):
    
    TEMPORAIRE = 0
    SORTANT = 1
    RESTANT= 2
    NOUVEAU = 3
    
    entity_names = [em.columns for em in entity_matrix]
    name2event = list()
    
    for i, en_i in enumerate(entity_names):
        print('chapitre ' + str(i) )
        name2event.append(dict())
        if i > 0 and i < (len(entity_names) - 1):
            for w in en_i:
                if w not in entity_names[i+1] and w not in entity_names[i-1]:
                    name2event[i][w] = TEMPORAIRE
                    print('     temporaire: ' + w)
                elif w not in entity_names[i+1] and w in entity_names[i-1]:
                    name2event[i][w] = SORTANT
                    print('     sortant: ' + w)
                elif w in entity_names[i+1] and w in entity_names[i-1]:
                    name2event[i][w] = RESTANT
                    print('     restant: ' + w)
                else:
                    name2event[i][w] = NOUVEAU
                    print('     nouveauté: ' + w )
    name2event[0] = {w: NOUVEAU for w in entity_names[0]}
    name2event[-1] = {w: SORTANT for w in entity_names[-1]}
    
    
    for k in range(len(entity_matrix)):
        mat = entity_matrix[k]
        entities_names = mat.columns
    
        G = nx.Graph()
        
        for j in range(len(entities_names)):
            edges = []
    
            for i in range(j):
                coef = mat.loc[entities_names[j], entities_names[i]]
                
                # Seuil de similarité entre entités
                if coef > 0.1:
                    edges.append((entities_names[j], entities_names[i], coef))
    
            G.add_weighted_edges_from(edges)
    
        pos = nx.spring_layout(G)
        nx.draw(G, pos, font_size=16, with_labels=False)
    
        # On décale le texte
        for p in pos:
            pos[p][1] += 0.07
        nx.draw_networkx_labels(G, pos)
        plt.title('Chapitre ' + str(k+1), fontweight='bold', fontdict={
            'fontsize': 15,
        })
        plt.show()