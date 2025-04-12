from pymongo import MongoClient

# Replace with your actual connection string
uri = "mongodb+srv://mongodb:fishoil@cluster0.isi7hy4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a client and connect to the server
client = MongoClient(uri)

# Access a specific database
db = client["talentscout"]

# Access a collection in that database
collection = db["candidates"]

# Insert a simple document

doc = {'name': 'gAAAAABn-kxx2x17aMJ1P78oierErbF2Yr5bu7czYgj5rWCWP67OQULwukpYMpHGM76bZPaLcB9zY8ROUi2RdYnGtWjHPgjyQA==', 'location': 'yes@gmail.com', 'tech_stack': ['python', 'java'], 'questions': ['Can you explain the concept of multiple inheritance in Python and Java, and discuss the issues that arise when implementing this feature?', 'How do you implement a lambda function in both Python and Java? Can you provide an example of where it would be useful to use a lambda function in both languages?', 'How would you implement a stack structure in both Python and Java? Can you discuss the time complexity of common stack operations and the class library functions available for stack implementation in both languages?', 'Explain the difference between an iterator and an iterable in Python, and an Iterator and an Iterable in Java. Can you provide examples demonstrating when you would use each, and how you would implement them in both languages?'], 'answers': ['idk', 'idk', 'idk', 'idk']}

result = collection.insert_one(doc)
print("Inserted ID:", result.inserted_id)

# Retrieve the document
#retrieved = collection.find_one({"_id": result.inserted_id})
#print("Retrieved Document:", retrieved)

