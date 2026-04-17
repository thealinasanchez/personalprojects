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
                folder_name VARCHAR(255) NOT NULL,
                creator_id INTEGER NOT NULL,
                FOREIGN KEY (creator_id) REFERENCES usernames(id)
            )
        ''')

    def getFolders(self):
        self.cursor.execute("""
            SELECT folders.id, folders.folder_name, folders.creator_id, usernames.username AS creator
            FROM folders
            JOIN usernames ON folders.creator_id = usernames.id
        """)
        folders = self.cursor.fetchall()
        return folders
    
    def getFolder(self, folder_id):
        data = [folder_id]
        self.cursor.execute("""
        SELECT folders.id, folders.folder_name, folders.creator_id, usernames.username AS creator
        FROM folders
        JOIN usernames ON folders.creator_id = usernames.id
        WHERE folders.id = ?
        """, data)
        folder = self.cursor.fetchone()
        return folder
    
    def createFolder(self, folder_name, creator_id):
        from usernamesdb import Usernames

        user = Usernames("usernames.db").getUsername(creator_id)
        if not user:
            return "User not found", 404

        data = [folder_name, creator_id]
        self.cursor.execute(
            "INSERT INTO folders (folder_name, creator_id) VALUES (?, ?)", data
        )
        self.connection.commit()

        return "Folder created successfully", 201
    
    def deleteFolder(self, folder_id):
        folder = self.getFolder(folder_id)
        if not folder:
            return "Folder not found", 404
        
        data = [folder_id]
        self.cursor.execute("DELETE FROM folders WHERE id = ?", data)
        self.connection.commit()
        return "Folder deleted successfully", 200
    
    def updateFolder(self, folder_id, folder_name):
        data = [folder_name, folder_id]
        self.cursor.execute("UPDATE folders SET folder_name = ? WHERE id = ?", data)
        self.connection.commit()
        return "Folder updated successfully", 200
    
    def getFlashcardsInFolder(self, folder_id):
        from flashcardsdb import FlashCards

        folder = self.getFolder(folder_id)
        if not folder:
            return "Folder not found", 404
        
        flashcards_db = FlashCards("flashcards.db")
        flashcards_db.cursor.execute(
            "SELECT * FROM flashcards WHERE folder_id = ?", [folder_id]
        )
        flashcards = flashcards_db.cursor.fetchall()

        if flashcards:
            return flashcards, 200
        else:
            return "No flashcards found in the folder", 404
        
    def getFoldersByCreatorId(self, creator_id):
        data = [creator_id]
        self.cursor.execute("""
            SELECT folders.id, folders.folder_name, folders.creator_id, usernames.username AS creator
            FROM folders
            JOIN usernames ON folders.creator_id = usernames.id
            WHERE folders.creator_id = ?
        """, data)
        folders = self.cursor.fetchall()

        if folders:
            return folders, 200
        else:
            return "No folders found for this user", 404