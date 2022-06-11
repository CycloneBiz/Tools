import pymongo
from tqdm import tqdm

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
        try:
            working = command(input(">>> "), database)
        except:
            print("A error occured")

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
        for i in tqdm(cmd[1:], desc="Packing"):
            with open(i) as f:
                package.append({
                    "filename": i,
                    "contents": f.read()
                })
        db.insert_many(package)
        print("Upload Finished")

    elif cmd[0] == "exit":
        print("Exiting...")
        return False
    return True

if __name__ == "__main__":
    main()