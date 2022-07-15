import pymongo
from tqdm import tqdm
import os

def main():
    print("Welcome to Cyclone Tools...\nCurrently OpenLoop only supports a URI string, not a certificate")

    uri = input("MongoDB URI (Leave empty if localhost): ")
    if uri == "" or uri == " ":
        uri = "mongodb://localhost:27017"

    print("Creating socket...")
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
    print("Getting server info...")
    info = client.server_info()
    print(f"Running MongoDB version {info.get('version', '((Error!))')}")
    
    database = input("Enter your database name (Leave empty if default): ")
    if database == "" or database == " ":
        database = "OpenLoop"
    database = client[database]["plugins"]

    print("Welcome to the CLI enviroment!\nCurrently, the enviroment does not support spaces in file names.")
    working = True
    while working:
        working = command(input(">>> "), database)

def command(cmd : str, db):
    cmd = cmd.split()
    if cmd[0] == "help":
        print("help - Shows help screen")
        print("rm   - Removes plugin")
        print("up   - Uploads plugin")
        print("ls   - Lists plugins")
        print("exit - Exits CLI")
        print("*    - Selects all")
    elif cmd[0] == "rm":
        if len(cmd)>1 and cmd[1] == "*" and input("Confirmation to delete all? (Y/N)").lower().startswith("y"):
            x = db.delete_many({})
            print(f"Deleted {x.deleted_count} plugins")
        elif len(cmd)>1:
            for i in tqdm(cmd[1:], desc="Deleting"):
                db.delete_one({"filename": i})
            print(f"Deleted {len(cmd[1:])} plugins")
    elif cmd[0] == "ls":
        for i in db.find():
            print(i["filename"])
    elif cmd[0] == "up":
        package = []
        if len(cmd) >= 2 and cmd[1] == "*":
            for i in os.listdir():
                if not i.startswith("."):
                    if i.count(".") == 1:
                        cmd.append(i)
        for i in tqdm(cmd[1:], desc="Packing"):
            if i!="*":
                with open(i) as f:
                    if db.find_one({"filename": i}):
                        db.delete_one({"filename": i})
                        print(" Overided file {}".format(i))
                    package.append({
                        "filename": i,
                        "contents": f.read()
                    })
        db.insert_many(package)
        print("Upload Finished")
    elif cmd[0] == "down" and len(cmd)==2:
        if cmd[1] == "*":
            files = list(db.find())
        else:
            files = list(db.find({"filename": cmd[1]}))
        
        if cmd[1]=="*" and files==[]:
            print("No plugins in Mongo")
        elif files==[]:
            print("Plugin does not exist")
        else:
            for i in files:
                with open(i["filename"], "w") as f:
                    f.write(i["contents"])
            print("Completed download")

    elif cmd[0] == "exit":
        print("Exiting...")
        return False
    return True

if __name__ == "__main__":
    main()