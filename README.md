## Schema/Pydantic Models
1. Schema/Pydantic Models define the structure of a request & response
2. This ensure that when a user wants to create a post, the request will only go through if it has a “title” and “content” in the body

## ORM Models:
1. Responsible for defining the columns of our “posts” table within postgres
2. Is used to query, create, delete, and update entries within the database
