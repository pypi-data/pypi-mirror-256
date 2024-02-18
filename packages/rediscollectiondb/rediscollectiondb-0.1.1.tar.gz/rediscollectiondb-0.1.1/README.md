
# RedisCollectionDB

## Description
RedisCollectionDB is a Python library that provides an easy-to-use interface for managing collections and their items within a Redis database. It allows for the addition and removal of collections and items, listing of current collections and items, and subscribes to changes in collections and items via Redis' publish/subscribe mechanism.

## Installation
Install RedisCollectionDB using pip:

```bash
pip install rediscollectiondb
```

## How to Use
First, ensure you have Redis running on your local machine or a server.

```python
from rediscollectiondb import RedisDB

# Initialize the RedisDB instance
db = RedisDB(db_name='your_database_name')

# Add a collection
db.add_collection('books')

# Add items to the collection
db.add_item('books', 'The Great Gatsby')
db.add_item('books', '1984')

# List collections
print(db.list_collections())

# List items in a collection
print(db.list_items('books'))

# Remove an item
db.remove_item('books', '1984')

# Remove a collection
db.remove_collection('books')
```

## Example
This example demonstrates adding a collection, adding items to it, and then listing and removing items and the collection.

```python
if __name__ == '__main__':
    db = RedisDB(db_name='myapp')

    db.add_collection('books')
    db.add_item('books', 'The Great Gatsby')
    db.add_item('books', '1984')

    print("Collections:", db.list_collections())
    print("Books items:", db.list_items('books'))

    db.remove_item('books', '1984')
    print("Books items after removal:", db.list_items('books'))

    db.remove_collection('books')
    print("Collections after removing books:", db.list_collections())
```
