
import redis
import threading
import json  # Import the json module for serialization

class RedisDB:
    def __init__(self, db_name, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)
        self.db_name = db_name
        self.pubsub = self.client.pubsub()  # Initialize a PubSub instance

    def add_collection(self, name):
        self.client.sadd(f'{self.db_name}:collections', name)
        self.on_collection_changed('add', name)

    def remove_collection(self, name):
        if self.client.srem(f'{self.db_name}:collections', name):
            for key in self.client.scan_iter(f"{self.db_name}:{name}:*"):
                self.client.delete(key)
            self.on_collection_changed('remove', name)

    def list_collections(self):
        return list(self.client.smembers(f'{self.db_name}:collections'))

    def add_item(self, collection, name):
        self.client.sadd(f"{self.db_name}:{collection}:items", name)
        self.on_item_changed('add', collection, name)

    def remove_item(self, collection, name):
        self.client.srem(f"{self.db_name}:{collection}:items", name)
        self.on_item_changed('remove', collection, name)

    def list_items(self, collection):
        return list(self.client.smembers(f"{self.db_name}:{collection}:items"))

    def on_item_changed(self, action, collection, item):
        message = {
            'action': action,
            'collection': collection,
            'item': item
        }
        # Serialize message to JSON string before publishing
        self.client.publish(f'{self.db_name}:item_changes', json.dumps(message))

    def on_collection_changed(self, action, collection):
        message = {
            'action': action,
            'collection': collection
        }
        # Serialize message to JSON string before publishing
        self.client.publish(f'{self.db_name}:collection_changes', json.dumps(message))

    def subscribe_to_changes(self):
        self.pubsub.subscribe([f'{self.db_name}:item_changes', f'{self.db_name}:collection_changes'])
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                # Deserialize message data from JSON string back to dictionary
                data = json.loads(message['data'].decode('utf-8'))
                print(f"Received message: {data}")

if __name__ == '__main__':
    db = RedisDB(db_name='myapp')  # Assumes Redis is running on localhost and default port

    # Start a thread to listen for changes
    def listen_for_changes(db_instance):
        db_instance.subscribe_to_changes()

    listener_thread = threading.Thread(target=listen_for_changes, args=(db,))
    listener_thread.start()

    # Perform some operations to trigger changes
    db.add_collection('books')
    db.add_item('books', 'The Great Gatsby')
    db.add_item('books', '1984')
