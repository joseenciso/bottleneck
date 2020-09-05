import os

os.environ["MONGO_URI"] = 'mongodb+srv://rootAccess:sP9eU2GAtnYugO53@posting-vndhj.mongodb.net/bottleneckdb?retryWrites=true&w=majority'
os.environ["MONGO_DBNAME"] = 'bottleneckdb'

# """
# client = pymongo.MongoClient("mongodb+srv://bottleneckAdmin:<password>@posting-vndhj.mongodb.net/<dbname>?retryWrites=true&w=majority")
# db = client.test

# Replace <password> with the password for the bottleneckAdmin user. Replace <dbname> with the name of the database that connections will use by default. Ensure any option params are URL encoded.

# Replace <password> with the password for the bottleneckAdmin user. Replace <dbname> with the name of the database that connections will use by default. Ensure any option params are URL encoded.
# """