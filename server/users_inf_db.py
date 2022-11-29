import pymongo

class DataBase(object):
    db_client = pymongo.MongoClient('mongodb://localhost:27017')
    current_db = db_client['wb_user_inf']
    collections = current_db['weather_brick_users_inf']

    def __init__(self, inf):
        self.inf = inf
    def check_email(self):
        return self.collections.find_one({'email': self.inf})
    def adding_user_inf(self):
        self.collections.insert_one(self.inf)
    def get_salt(self):
        try:
            return self.collections.find_one({'email': self.inf})['salt']
        except:
            return 'None'
    def log_in(self):
        if self.collections.find_one({'email': self.inf['email']})['password'] == self.inf['password']:
            inf = self.collections.find_one({'email': self.inf['email']})
            del inf['salt'], inf['password'], inf['_id']
            return inf