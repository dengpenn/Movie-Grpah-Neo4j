# Graph-For-Movie

Building the graph database based on the `neo4j` using `MovieLen10M` dataset.

## Load the data
Based on the test, `neo4j-admin import` is the most efficient way to insert your data into the database. We also try to insert the data using the `create` clause. The comparsion of speed is shown below.

| Method  | Speed |
|-----|-----|
| Neo4j-admin import | 10M/10s  | 
|  calcu_time_2   |   10K/70S  | 
|   calculate_time.py  |  10k/1min   |

## Prepare your data

`neo4j-admin import` requires to use a new database. You need to assign a value to `--database`(the default `--graph.db`) may not work.
After creating the ``, you need to switch the database in the `./conf/neo4j.conf` file which is `dbms.active_database=some_database.db`.

To make the `import` command work, the data should look like this:

| id:ID(movie-id) | name                        | 
|-----------------|-----------------------------| 
| 1               | Toy Story                   | 
| 2               | Jumanji                     | 
| 3               | Grumpier Old Men            | 
| 4               | Waiting to Exhale           | 
| 5               | Father of the Bride Part II | 
| 6               | Heat                        | 
| 7               | Sabrina                     | 

| id:ID(user-id) | 
|----------------| 
| 1              | 
| 2              | 
| 3              | 
| 4              | 
| 5              | 
| 6              | 
| 7              | 

Because the movie_id and user_id both are sequenal identifier and many of them have some value, so id space like `(user-id)` and `(movie-id)` are needed.

The csv file should look like this:

| :START_ID(user-id) | ratings | :END_ID(movie-id) | :TYPE   | 
|--------------------|---------|-------------------|---------| 
| 1                  | 5       | 122               | RATINGS | 
| 1                  | 5       | 185               | RATINGS | 
| 1                  | 5       | 231               | RATINGS | 
| 1                  | 5       | 292               | RATINGS | 
| 1                  | 5       | 316               | RATINGS | 
| 1                  | 5       | 329               | RATINGS | 
| 1                  | 5       | 355               | RATINGS | 
| 1                  | 5       | 356               | RATINGS | 
| 1                  | 5       | 362               | RATINGS | 

The relationship between the user and movie are called `RATINGS` and scores which is the property of `RATINGS` is given by `ratings` field.


