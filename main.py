# import home-made modules
from preprocess import load_corpus, preprocess
from termdocumentmatrix import get_termDocumentMatrix
from named_entities import get_named_entities, filter_entities
from entity_matrix import get_entity_matrix
from topics import get_topics
from graph_relations import draw_entities_relation


def main():
    print('Loading corpus...')
    chapters = load_corpus()

    print('Finding named entities...')
    entities_list = get_named_entities(chapters)
    entities_list = filter_entities(entities_list)

    print('Processing corpus...')
    chapters_processed = preprocess(chapters)

    print('Creating TermDocumentMatrix...')
    vocabulary, vector_space = get_termDocumentMatrix(chapters_processed)

    print('Computing entities relationships...')
    entity_matrix = get_entity_matrix(entities_list, vocabulary, vector_space)
    
    print('Topic extraction...')
    topics = get_topics(chapters_processed)

    print('Entities graph...')
    draw_entities_relation(entity_matrix, topics)


if __name__ == '__main__':
    main()
