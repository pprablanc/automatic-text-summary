import numpy as np
from scipy.sparse import csr_matrix
import re

import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from nltk.corpus import stopwords


def get_entity_matrix(entities_list, vocabulary, vector_space):
	entity_matrix = []

	stop = set(stopwords.words('english'))
	stop.add('shall')
	stop.add('said')
	stop.add('ah')
	stop.add('oh')
	stop.add('ahah')

    
	# Pour chaque chapitre
	for k in range(len(entities_list)):
		d = dict()

		print("Chapitre ", k)

		# Pour l'entité j
		for j in range(len(entities_list[k])):
			tmp_res = []

			# On la décompose en unigramme sans ponctuation pour coller au vocabulaire
			entity1 = [word for word in re.sub(r'[^\w\s]+', '', entities_list[k][j]).lower().split() if word not in stop]
			
			vectors_e1 = []
			for word in entity1:
				try:
					vectors_e1.append(vector_space[k][vocabulary[k][word],:])
				except:
					continue
					
			v1 = np.sum(vectors_e1, axis=0)

			# Pour l'entité i
			for i in range(len(entities_list[k])):
				# On la décompose en unigramme
				entity2 = [word for word in re.sub(r'[^\w\s]+', '', entities_list[k][i]).lower().split() if word not in stop]
				#entity2 = [word for word in entity2 if word not in stop]
				# On récupère le vecteur BOW associé à chacun
				
				vectors_e2 = []
				for word in entity2:
					try:
						vectors_e2.append(vector_space[k][vocabulary[k][word],:])
					except:
						continue

				v2 = np.sum(vectors_e2, axis=0)
				
				# Un des vecteurs peut ne pas avoir été trouvé dans le vocabulaire
				try:
					A = np.array([v1, v2]).reshape(2, v1.shape[1])

					# On calcule la similarité cosinus entre un token de chaque entité
					tmp_res.append(cosine_similarity(A)[0,1])
				except:
					tmp_res.append(0.)

			d[entities_list[k][j]] = pd.Series(tmp_res, index=entities_list[k])

		# On passe la matrice en dataframe pour avoir les noms de colonnes
		entity_matrix.append(pd.DataFrame(d))

	return entity_matrix