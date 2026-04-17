from flask import Flask, request, jsonify
from flask_cors import CORS
from flashcardsdb import FlashCards
from usernamesdb import Usernames
from foldersdb import Folders

app = Flask(__name__)
CORS(app)

class MyFlask(Flask):
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        super().add_url_rule(rule, endpoint, view_func, provide_automatic_options=False, **options)

@app.route("/<path:path>", methods=["OPTIONS"])
def cors_preflight(path):
    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }
    return "", 204, response_headers

#
#
### FLASHCARDS SECTION ###
#
#

@app.route("/flashcards", methods=["GET"])
def retrieve_flashcards():
    db = FlashCards("flashcards.db")
    flashcards = db.getFlashcards()
    return flashcards, 200, {"Access-Control-Allow-Origin": "*"}

@app.route("/flashcards/<int:flashcard_id>", methods=["GET"])
def retrieve_flashcard_member(flashcard_id):
    db = FlashCards("flashcards.db")
    flashcard = db.getFlashcard(flashcard_id)
    if flashcard:
        return flashcard, 200, {"Access-Control-Allow-Origin": "*"}
    else:
        return "Flashcard Not Found", 404, {"Access-Control-Allow-Origin": "*"}

@app.route("/flashcards", methods=["POST"])
def add_to_flashcards():
    try:
        db = FlashCards("flashcards.db")

        # check if all required fields are present in the request
        required_fields = ["term", "definition", "folder_id"]
        for field in required_fields:
            if field not in request.form:
                return f"Missing required field: {field}", 400, {"Access-Control-Allow-Origin": "*"}

        # extract data from the request
        term = request.form["term"]
        definition = request.form["definition"]
        folder_id = int(request.form["folder_id"])

        # create the flashcard in the database
        db.createFlashcard(term, definition, folder_id)
        return "Created", 201, {"Access-Control-Allow-Origin": "*"}
    except Exception as e:
        return f"An error occurred: {str(e)}", 500, {"Access-Control-Allow-Origin": "*"}
    
@app.route("/flashcards/<int:flashcard_id>", methods=["DELETE"])
def delete_flashcard(flashcard_id):
    try:
        db = FlashCards("flashcards.db")
        result_message = db.deleteFlashcard(flashcard_id)
        return  result_message, 200, {"Access-Control-Allow-Origin":"*"}
    except Exception as e:
        return f"An error occurred: {str(e)}", 500, {"Access-Control-Allow-Origin":"*"}

@app.route("/flashcards/<int:flashcard_id>", methods=["PUT"])
def update_flashcard(flashcard_id):
    db = FlashCards("flashcards.db")
    flashcard = db.getFlashcard(flashcard_id)
    if flashcard:
        term = request.form["term"]
        definition = request.form["definition"]

        if term is None or definition is None:
            return "Missing required fields", 400, {"Access-Control-Allow-Origin": "*"}

        db.updateFlashcard(term, definition, flashcard_id)
        return "Flashcard updated successfully", 200, {"Access-Control-Allow-Origin":"*"}
    else:
        return "Flashcard not found", 404, {"Access-Control-Allow-Origin":"*"}

#
#
### USERNAME SECTION ###
#
#
    
@app.route("/usernames", methods=["GET"])
def retrieve_usernames():
    try:
        db = Usernames("usernames.db")
        usernames = db.getUsernames()
        print("Retrieve usernames:", usernames)
        return usernames, 200, {"Access-Control-Allow-Origin":"*"}
    except Exception as e:
        return f"An error occurred: {str(e)}", 500, {"Access-Control-Allow-Origin":"*"}

@app.route("/usernames/<int:username_id>", methods=["GET"])
def retrieve_username_member(username_id):
    db = Usernames("usernames.db")
    username = db.getUsername(username_id)
    if username:
        return username, 200, {"Access-Control-Allow-Origin":"*"}
    else:
        return "Username not found", 404, {"Access-Control-Allow-Origin":"*"}

@app.route("/usernames", methods=["POST"])
def add_to_usernames():
    try:
        db = Usernames("usernames.db")

        # check if all required fields are present in the request
        if "username" not in request.form:
            return "Missing required field: username", 400, {"Access-Control-Allow-Origin": "*"}
        
        username = request.form["username"]

        result, status_code = db.createUsername(username)

        return result, status_code, {"Access-Control-Allow-Origin": "*"}

    except Exception as e:
        return f"An error occurred: {str(e)}", 500, {"Access-Control-Allow-Origin":"*"}

@app.route("/usernames/<int:username_id>", methods=["DELETE"])
def delete_username(username_id):
    db = Usernames("usernames.db")
    username = db.getUsername(username_id)
    print(username)
    if username:
        db.deleteUsername(username_id)
        return "Username deleted successfully", 200, {"Access-Control-Allow-Origin":"*"}
    else:
        return "Username not found", 404, {"Access-Control-Allow-Origin":"*"}

@app.route("/usernames/<int:username_id>", methods=["PUT"])
def update_username(username_id):
    db = Usernames("usernames.db")
    username = db.getUsername(username_id)
    if username:
        username = request.form["username"]
        folderlist = request.form["folderlist"]

        db.updateUsername(username, folderlist, username_id)
        return "Username updated successfully", 200, {"Access-Control-Allow-Origin":"*"}
    else:
        return "Username not found", 404, {"Access-Control-Allow-Origin":"*"}

@app.route('/usernames/<int:user_id>/folders', methods=["GET"])
def get_user_folders(user_id):
    db = Folders("folders.db")
    
    result, status_code = db.getFoldersByCreatorId(user_id)

    if status_code == 200:
        return jsonify(result), 200, {"Access-Control-Allow-Origin": "*"}
    return result, status_code, {"Access-Control-Allow-Origin": "*"}

#
#
### FOLDERS SECTION ###
#
#

@app.route("/folders", methods=["GET"])
def retrieve_folders():
    db = Folders("folders.db")
    folders = db.getFolders()
    return folders, 200, {"Access-Control-Allow-Origin":"*"}

@app.route("/folders/<int:folder_id>", methods=["GET"])
def retrieve_folder_member(folder_id):
    db = Folders("folders.db")
    folder = db.getFolder(folder_id)
    if folder:
        return folder, 200, {"Access-Control-Allow-Origin":"*"}
    else:
        return "Folder not found", 404, {"Access-Control-Allow-Origin":"*"}

@app.route("/folders", methods=["POST"])
def add_to_folders():
    db = Folders("folders.db")
    if "folder_name" not in request.form or "creator_id" not in request.form:
        return "Missing required field: folder_name or creator_id", 400, {"Access-Control-Allow-Origin":"*"}

    folder_name = request.form["folder_name"]
    creator_id = int(request.form["creator_id"])

    result, status_code = db.createFolder(folder_name, creator_id)
    return result, status_code, {"Access-Control-Allow-Origin":"*"}

@app.route("/folders/<int:folder_id>", methods=["DELETE"])
def delete_folder(folder_id):
    db = Folders("folders.db")
    result, status_code = db.deleteFolder(folder_id)
    return result, status_code, {"Access-Control-Allow-Origin":"*"}

@app.route("/folders/<int:folder_id>", methods=["PUT"])
def update_folder(folder_id):
    try:
        db = Folders("folders.db")

        if "folder_name" not in request.form:
            return "Missing required field: folder_name", 400, {"Access-Control-Allow-Origin":"*"}

        folder_name = request.form["folder_name"]

        result, status_code = db.updateFolder(folder_id, folder_name)
        return result, status_code, {"Access-Control-Allow-Origin":"*"}
    except Exception as e:
        return f"An error occurred: {str(e)}", 500, {"Access-Control-Allow-Origin": "*"}

@app.route("/folders/<int:folder_id>/flashcards", methods=["GET"])
def retrieve_flashcards_in_folder(folder_id):
    db = Folders("folders.db")
    
    result, status_code = db.getFlashcardsInFolder(folder_id)

    if status_code == 200:
        return jsonify(result), 200, {"Access-Control-Allow-Origin": "*"}
    return result, status_code, {"Access-Control-Allow-Origin": "*"}

def run():
    app.run(port=8080)

if __name__ == '__main__':
    run()