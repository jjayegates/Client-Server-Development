from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, usr="aacuser", pwd="2023Graduate"):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections. 
        self.client = MongoClient('mongodb://%s:%s@localhost:55372/AAC' % (usr, pwd))
        # where xxxx is your unique port number
        self.database = self.client['AAC']

    # Complete this create method to implement the C in CRUD.
    def create(self, data):
        #self.database.animals.insert_many(data) 
        if data is not None:
            try:
                if type(data) == list:
                    self.database.animals.insert_many(data) 
                else:
                    self.database.animals.insert_one(data) 
                return True
            except:
                return False 
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    # Read method to implement the R in CRUD.
    def read(self, key_value_pairs):  #  key_value_pairs should be a dictionary 
        if key_value_pairs is not None:
            #  run the find function with the supplied key value pairs 
            results = self.database.animals.find(key_value_pairs,{"_id":False}) 
            return results 
        else:
            raise Exception("Nothing to find, because key_value_pairs parameter is empty")
            
    # Read method to implement the R in CRUD.
    def update(self, my_filter, new_values):  #  key_value_pairs should be a dictionary 
        if my_filter is not None and new_values is not None:
            #  run the find function with the supplied filter and new values 
            #  my_filter should be of the format:  { "field": "value" }
            #  new_values should be of the format:  { "$set": { "field": "new value" } }

            return self.database.animals.update_many(my_filter, new_values)
        else:
            raise Exception("Nothing to update, because my_filter or new_values parameter is empty")
            
    # Read method to implement the D in CRUD.
    def delete(self, key_value_pairs):  #  key_value_pairs should be a dictionary 
        if key_value_pairs is not None:
            #  run the find function with the supplied key value pairs 
            return self.database.animals.delete_many(key_value_pairs)
        else:
            raise Exception("Nothing to delete, because key_value_pairs parameter is empty")