from py2neo import Graph


graph = Graph(password='fighting33')


'''
1) Write a query that finds average rating of each movie.

2) Write a query that finds users who are similar to a given user (target user), the id of the target user is an input parameter.  Users are similar to the target user if they rate the same movies.

3) Write a query that finds to number of movies in each genre.

4) Write 3 different queries of your choice to demonstrate that your data storage is working.

# average rating of user
# find the movies of name which receive the most rating
# find the movies which receive the highest average rating
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
    for each_movie in range(150):
        ratings_number = graph.run('match (u:User)-[:RATINGS]->(m:Movie{id:\'%s\'}) return count(u)' % each_movie).data()[0]['count(u)']
        movie_rating[each_movie] = int(ratings_number)

    maximum = max(movie_rating, key=movie_rating.get)  # Just use 'min' instead of 'max' for minimum.
    movie_name = graph.run('match (m:Movie{id:\'%s\'}) return (m.name)' % maximum).data()[0]['(m.name)']
    return movie_name


def task_6():
    movie_rating = {}
    movie_length = graph.run('match (m:Movie) return count(m)').data()[0]['count(m)']
    for each_movie in range(150):
        ratings_number = graph.run('match (u:User)-[r:RATINGS]->(m:Movie{id:\'%s\'}) return avg(tofloat(r.rating))' % each_movie).data()[0]['avg(tofloat(r.rating))']
        # ['avg(tofloat(count(u))']
        if ratings_number is None:
            ratings_number = 0
        movie_rating[each_movie] = float(ratings_number)

    maximum = max(movie_rating, key=movie_rating.get)  # Just use 'min' instead of 'max' for minimum.
    movie_name = graph.run('match (m:Movie{id:\'%s\'}) return (m.name)' % maximum).data()[0]['(m.name)']
    print(movie_name)
    print('Higest Rating is')
    print(movie_rating[maximum])

if __name__ == '__main__':
    task_6()
    # task_4(1)
    # task_2(1)

    '''
    # Answer 3
    answer_1 = task_3()
    for k in answer_1.keys():
        print(k + ":" + str(answer_1[k][0]['count (m)']))
    '''