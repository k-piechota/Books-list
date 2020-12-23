import os
import app
from mongoengine import connect, disconnect


class TestApp:
    def __enter__(self):
        self.old_environ = os.environ
        os.environ = os.environ.copy()

        connect('mongoenginetest', host='mongomock://localhost')
        self.app = app.create_app().test_client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.environ = self.old_environ
        disconnect()
