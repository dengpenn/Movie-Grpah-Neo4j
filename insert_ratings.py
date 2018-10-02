from py2neo import Graph, Node, Relationship
import timeit


user_list = []
def read_file_by_line(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        while True:
            data = f.readline()
            if not data:
                break
            yield data


def insert_rating(node_id, rating, node_movie, tx):
    rel = Relationship(node_id, 'RATINGS', node_movie, rating=rating)
    tx.create(rel)
    tx.commit()


def main():
    # Can I keep the user_node
    graph = Graph(password='fighting33')
    text_generator = read_file_by_line('./ml-10M100K/test.dat')
    # for text in text_generator:
    for text in text_generator:
        splitted_text = text.split('::')
        user_id, movie_id, ratings = splitted_text[0:3]
        movie_node = graph.nodes.match("Movie", id=movie_id).first()
        if user_id not in user_list:
            user_node = Node("User", id=user_id)
            user_list.append(user_id)
            tx = graph.begin()
            insert_rating(user_node, ratings, movie_node, tx)
        else:
            user_node = graph.nodes.match("User", id=user_id).first()
            tx = graph.begin()
            insert_rating(user_node, ratings, movie_node, tx)

if __name__ == '__main__':
    # 10000 for 77s
    start = timeit.default_timer()
    main()
    end = timeit.default_timer()
    print(end - start)