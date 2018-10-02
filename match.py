from py2neo import Graph


graph = Graph(password='fighting33')


'''
1) Write a query that finds average rating of each movie.

2) Write a query that finds users who are similar to a given user (target user), the id of the target user is an input parameter.  Users are similar to the target user if they rate the same movies.

3) Write a query that finds to number of movies in each genre.

4) Write 3 different queries of your choice to demonstrate that your data storage is working.

# average rating of user
# find the movies of name which receive the most rating
# find the movies which receive the highest rating
'''

def task_1():
    movie_ratings_list = []
    ratings = graph.run('match (u:User)-[r:RATINGS]->(m:Movie{id:\'1\'}) return (r.rating)').data()
    for rating in ratings:
        movie_ratings_list.append(float(rating['(r.rating)']))
    print(sum(movie_ratings_list))
    print(sum(movie_ratings_list) / float(len(movie_ratings_list)))


def task_2(user_id):
    movie_list = []
    movies = graph.run('match (u:User{id:\'%s\'})-[r:RATINGS]->(m:Movie) return (m.id)' % user_id)
    for m in movies:
        movie_list.append(m['(m.id)'])

    similar_user = []
    for movie_id in movie_list:
        user = graph.run('match (u:User)-[r:RATINGS]->(m:Movie{id:\'%s\'}) return (u.id)' % movie_id).data()
        for u in user:
            similar_user.append(u['(u.id)'])
    user_set = set(similar_user)
    return user_set

    # ratings = graph.run('match (u:User)-[r:RATINGS]->(m:Movie{id:\'1\'}) return (r.rating)').data()


def task_3():
    genre_number = {}
    genre_data = graph.run('match (g:Genre) return (g.type)').data()
    genre_list = [g['(g.type)'] for g in genre_data]

    for g in genre_list:
        movie_number = graph.run('match (m:Movie)-[:BELONGS_TO]->(:Genre{type:\'%s\'}) return count (m)' % g).data()
        genre_number[g] = movie_number

    return genre_number


def task_4(user_id):
    ratings = graph.run('match (u:User{id:\'%s\'})-[r:RATINGS]->(m:Movie) return avg(TOFLOAT(r.rating))' % user_id).data()
    return ratings[0]['avg(TOFLOAT(r.rating))']


def task_5():
    movie_rating = {}
    movie_length = graph.run('match (m:Movie) return count(m)').data()[0]['count(m)']
    for each_movie in range(movie_length):
        ratings_number = graph.run('match (u:User)-[:RATINGS]->(m:Movie{id:\'%s\'}) return count(u)' % each_movie).data()[0]['count(u)']
        movie_length[each_movie] = int(ratings_number)
    return movie_rating

def task_6():
    pass



if __name__ == '__main__':
    temp = task_5()
    # task_4(1)
    # task_2(1)

    '''
    # Answer 3
    answer_1 = task_3()
    for k in answer_1.keys():
        print(k + ":" + str(answer_1[k][0]['count (m)']))
    '''