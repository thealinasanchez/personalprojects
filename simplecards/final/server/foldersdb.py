import sqlite3

def dict_factory(cursor, row):
    # fields represent column headers
    fields = []
    
    for column in cursor.description:
        # adding column headers to the fields list
        fields.append(column[0])

    result_dict = {}
    for i in range(len(fields)):
        result_dict[fields[i]] = row[i]
    return result_dict

class Folders:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folder_name  VARCHAR(255),
                creator TEXT,
                flashcard_list TEXT
            )
        ''')

    def getFolders(self):
        self.cursor.execute("SELECT * FROM folders")
        folders = self.cursor.fetchall()
        return folders
    
    def getFolder(self, folder_id):
        data = [folder_id]
        self.cursor.execute("SELECT * FROM folders WHERE id = ?", data)
        folder = self.cursor.fetchone()
        return folder
    
    def createFolder(self, folder_name, creator_id):
        from usernamesdb import Usernames

        # get the username of the creator based on creator_id
        creator = Usernames("usernames.db").getUsername(creator_id)['username']
        flashcard_list = ""

        # insert folder into the folders table
        data = [folder_name, creator, flashcard_list]
        self.cursor.execute("INSERT INTO folders (folder_name, creator, flashcard_list) VALUES (?,?,?)", data)
        self.connection.commit()

        # retrieve the id of the newly created folder
        folder_id = self.cursor.lastrowid

        # add the new folder id to the creator's folderlist
        Usernames("usernames.db").addFolderToFolderlist(creator_id, folder_id)

        return "Folder created successfully", 201
    
    def deleteFolder(self, folder_id):
        from usernamesdb import Usernames

        data = [folder_id]

        # delete the folder from the folders table
        self.cursor.execute("DELETE FROM folders WHERE id = ?", data)
        self.connection.commit()

        # delete the folder id from the creator's folderlist
        Usernames("usernames.db").deleteFolderFromFolderlist(folder_id)
        return "Folder deleted successfully", 200
    
    def updateFolder(self, folder_id, folder_name):
        data = [folder_name, folder_id]
        self.cursor.execute("UPDATE folders SET folder_name = ? WHERE id = ?", data)
        self.connection.commit()
        return "Folder updated successfully", 200
    
    def addFlashcardToFolder(self, folder_id, flashcard_id):
        folder = self.getFolder(folder_id)
        if folder:
            flashcard_list = folder['flashcard_list']
            if flashcard_list:
                flashcard_list += f",{flashcard_id}"
            else:
                flashcard_list = str(flashcard_id)
            data = [flashcard_list, folder_id]
            self.cursor.execute("UPDATE folders SET flashcard_list = ? WHERE id = ?", data)
            self.connection.commit()
            return "Flashcard added to folder successfully", 200
        else:
            return "Folder not found", 404
    
    def getFlashcardsInFolder(self, folder_id):
        from flashcardsdb import FlashCards

        flashcards = []
        folder = self.getFolder(folder_id)
        if folder:
            flashcard_list = folder['flashcard_list']
            if flashcard_list:
                flashcard_ids = flashcard_list.split(',')
                flashcards_db = FlashCards("flashcards.db")
                for flashcard_id in flashcard_ids:
                    flashcard = flashcards_db.getFlashcard(int(flashcard_id))
                    if flashcard:
                        flashcards.append(flashcard)
                return flashcards
            else:
                return "No flashcards found in the folder", 404
        else:
            return "Folder not found", 404

    def removeFlashcardFromFolder(self, folder_id, flashcard_id):
        folder = self.getFolder(folder_id)
        if folder:
            flashcard_list = folder['flashcard_list']
            if flashcard_list:
                flashcard_ids = flashcard_list.split(',')
                if str(flashcard_id) in flashcard_ids:
                    flashcard_ids.remove(str(flashcard_id))
                    new_flashcard_list = ','.join(flashcard_ids)
                    data = [new_flashcard_list, folder_id]
                    self.cursor.execute("UPDATE folders SET flashcard_list = ? WHERE id = ?", data)
                    self.connection.commit()
                    return "Flashcard removed from folder successfully"
                else:
                    return "Flashcard not found in folder"
            else:
                return "No flashcards found in the folder"
        else:
            return "Folder not found"