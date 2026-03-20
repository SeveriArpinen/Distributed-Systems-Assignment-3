import xmlrpc.client

server = "http://127.0.0.1:5000"

def main():

    # COnnecting to the server
    proxy = xmlrpc.client.ServerProxy(server, allow_none=True)

    print("Welcome to the notebook!")
    #while loop for menu
    while True:
        print("1) Add a new topic or a note to an existing topic")
        print("2) Print all topics")
        print("3) Print one topic")
        print("0) Exit")
        inpt = input("Type your choise: ").strip()
        print("\n")

        if inpt == "1":
            name = input("Input topic name: ").strip()
            note_name = input("Input note name: ").strip()
            text = input(f"Text for {name}: ").strip()
            try:
                proxy.add_note(name, note_name, text)
                print("Note added!")
                print("\n")
            except Exception as e:
                print("There was an error adding the topic: ", e)
                print("\n")

        elif inpt == "2":
            try:
                topics = proxy.get_topics()
                print("Topics: ", topics)
                print("\n")
            except Exception as e:
                print("Error getting topics:", e)

        elif inpt == "3":
            name = input("Topic name: ").strip()
            entries = proxy.print_topic(name)
            if entries:
                for entry in entries:
                    print("Note name:", entry["name"])
                    print("Text:", entry["text"])
                    print("Timestamp:", entry["timestamp"])
                    print("\n")
            else:
                print("Topic not found")
                print("\n")

        elif inpt == "0":
            print("Closing connection!")
            print("\n")
            break

        else:
            print("Wrong input, try again")
            print("\n")

main()