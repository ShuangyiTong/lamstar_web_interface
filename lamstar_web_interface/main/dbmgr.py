import sqlite3
from threading import Lock

class DBMgr:

    def __init__(self):
        # a dict use internal_id as key, connection object as value
        self.conns = {}
        # since we allow shared connection between thread, we want to have locks
        self.locks = {}

    def establish_connection(self, db_type, internal_id):
        db_path = 'main/databases/' + internal_id + '.db'
        if internal_id not in self.conns.keys():
            if db_type == 'SQLite3':
                conn = sqlite3.connect(db_path, check_same_thread=False)
                self.conns[internal_id] = conn
                # create lock
                self.locks[internal_id] = Lock()
            else:
                return [0, 'Database type undefined']
        else:
            return [1, 'Connection already established']
        return [1, 'Connection established']

    def commit(self, internal_id):
        if internal_id not in self.conns.keys():
            return [0, 'Connection not exists']
        elif self.locks[internal_id].acquire(timeout=5):
            self.conns[internal_id].commit()
            self.locks[internal_id].release()
            return [1, 'Committment successful']
        else:
            return [-1, 'Cannot get lock now for this database ' + internal_id]

    def close(self, internal_id):
        if internal_id not in self.conns.keys():
            return [0, 'Connection not exists']
        elif self.locks[internal_id].acquire(timeout=5):
            self.conns[internal_id].close()
            del self.conns[internal_id]
            del self.locks[internal_id]
            return [1, 'Connection closed']
        else:
            return [-1, 'Cannot get lock now for this database ' + internal_id]

dbmgr = DBMgr()

# functions exposed to peripheral modules

def active_connections():
    return dbmgr.conns.keys()

def close_connection(internal_id):
    return dbmgr.close(internal_id)