import os
from models.engine.db_storage import DBStorage  # type: ignore

storage = DBStorage()
storage.reload()
