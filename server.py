from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as Tree
from datetime import datetime

database = "database.xml"

def get_data():
    # get data from database file
    tree = Tree.parse(database.xml)
    root = tree.getroot()
    return tree, root

def main():
    server = SimpleXMLRPCServer(("127.0.0.1, 5000"), allow_none=True) #start server on localhost:5000


    print("server running on 127.0.0.1:5000")
    server.serve_forever()

main()