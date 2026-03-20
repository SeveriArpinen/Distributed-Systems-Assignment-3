from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as Tree
from datetime import datetime
from socketserver import ThreadingMixIn
import threading

database = "database.xml"
database_lock = threading.Lock() #Lock for add_note, so only one thread can write at a time

# make xmlrpc server threaded, handles each request in separate thread
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

def get_data():
    # get data from database file
    # this would be a database in a real system, now using just a simple file database.xml
    # try catch if the file does not exist
    try:
        tree = Tree.parse(database)
        root = tree.getroot()
    except (FileNotFoundError, Tree.ParseError): # file not found or cant parse the xml tree, create data root and write the file
        root = Tree.Element("data")
        tree = Tree.ElementTree(root)
        tree.write(database, encoding="utf-8", xml_declaration=True)
    return tree, root

def get_topic(root, name):
    # gets one topic from database from topic name
    for topic in root.findall("topic"):
        if topic.get("name") == name: # if topic matches name searhed
            return topic
    return None # else return none

def save(tree):
    # save current changes to database
    tree.write(database, encoding="utf-8", xml_declaration=True)

def append_topic(topic, note_name, text):
    # function to add a new note + timestamp for a topic that exist
    time = datetime.now().strftime("%d/%m/%Y, %H:%M")

    note = Tree.SubElement(topic, "note", {"name": note_name}) # creates new note
    text_append = Tree.SubElement(note, "text") # creates new text for note
    text_append.text = text # append text

    time_append = Tree.SubElement(note, "timestamp")
    time_append.text = time

def create_topic(root, name, note_name, text):
    # make a new topic and add note
    topic = Tree.SubElement(root, "topic", {"name": name})
    append_topic(topic, note_name, text)

def add_note(name, note_name, text):
    # function for getting first the data from xml
    # check if topic already exist -> if does append, if doesnt -> add a new topic
    # uses database_lock, so only one thread can write at a time, multiple writes can break the file
    with database_lock:
        tree, root = get_data()

        topic = get_topic(root, name)
        if topic is not None: #check if exists
            append_topic(topic, note_name, text)
            save(tree) 
            return f"Appended text for topic: {name}"
        
        create_topic(root, name, note_name, text)
        save(tree)
        return f"New topic created, {name}"

def get_topics():
    # function that returns all topic names
    tree, root = get_data()
    names = [] #array for topic names
    for topic in root.findall("topic"):
        names.append(topic.get("name",""))
    return names

def print_topic(name):
    # fucntion for printing notes for a topic
    tree, root = get_data()
    topic = get_topic(root, name)

    if topic is None: # if empty or doesnt exist
        return []
    
    entries = []
    for note in topic.findall("note"):
        entries.append({"name": note.get("name",""), "text": note.findtext("text",""), "timestamp": note.findtext("timestamp", "")})
    return entries

def main():
    #starts threaded xmlrpc server and functions for client
    server = ThreadedXMLRPCServer(("127.0.0.1", 5000), allow_none=True) #start server on localhost:5000
    server.register_function(add_note, "add_note")
    server.register_function(get_topics, "get_topics")
    server.register_function(print_topic, "print_topic")

    print("server running on 127.0.0.1:5000")
    server.serve_forever() #start request loop, each rpc request handled in own thread

main()