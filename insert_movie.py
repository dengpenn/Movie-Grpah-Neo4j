from py2neo import Graph, Node, Relationship
from subprocess import call
import re


YEAR_PATTERN = re.compile('\(\d{4}\)')
existing_genre = []

def init():
    call(['cd ~/Downloads/neo4j-community-3.4.7/bin;./neo4j start'], shell=True)
    graph = Graph(password='fighting33')
    return graph


def stop():
    call(['cd ~/Downloads/neo4j-community-3.4.7/bin;./neo4j stop'], shell=True)


def process_genre(text):
    # 1::Toy Story (1995)::Adventure|Animation|Children|Comedy|Fantasy
    split_text = text.split("::")
    id = split_text[0]
    name = YEAR_PATTERN.split(split_text[1])[0].strip()
    genre = split_text[-1].split('\n')[0].split("|")
    return id, name, genre


def create_relation(node_a, node_b, tx):
    node_ab = Relationship(node_a, 'BELONGS_TO', node_b)
    tx.create(node_ab)
    tx.commit()


def insert_into_graph(node_a_id, node_a_name, genre_list, graph):
    tx = graph.begin()
    node_a = Node("Movie", id=node_a_id, name=node_a_name)
    for g in genre_list:
        if g in existing_genre:
            node_b = graph.nodes.match("Genre", type=g).first()
            create_relation(node_a, node_b, tx)
            tx = graph.begin()
        else:
            node_b = Node("Genre", type=g)
            create_relation(node_a, node_b, tx)
            tx = graph.begin()

    for g in genre_list:
        if g not in existing_genre:
            existing_genre.append(g)

def open_file(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        texts = f.readlines()
    return texts


if __name__ == '__main__':
    graph = Graph(password='fighting33')
    graph.delete_all()
    # graph = init()
    texts = open_file('./ml-10M100K/movies.dat')
    for text in texts:
        id, name, genre = process_genre(text)
        insert_into_graph(id, name, genre, graph)
        print(id)
    # stop()
# GoldenEye