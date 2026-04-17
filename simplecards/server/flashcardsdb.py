import sqlite3
from usernamesdb import Usernames
from foldersdb import Folders

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

class FlashCards:
    def __init__(self, filename):
        # connect to DB file
        self.connection = sqlite3.connect(filename)
        self.connection.row_factory = dict_factory
        self.usernames_db = Usernames("usernames.db")
        self.folders_db = Folders("folders.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT NOT NULL,
                definition TEXT NOT NULL,
                folder_id INTEGER,
                FOREIGN KEY (folder_id) REFERENCES folders(id)
            )
        ''')
    
    def getFlashcards(self):
        self.cursor.execute("SELECT * FROM flashcards")
        flashcards = self.cursor.fetchall()
        return flashcards
    
    def getFlashcard(self, flashcard_id):
        data = [flashcard_id]
        self.cursor.execute("SELECT * FROM flashcards WHERE id = ?", data)
        flashcard = self.cursor.fetchone()
        return flashcard
    
    def createFlashcard(self, term, definition, folder_id):
        folder = self.folders_db.getFolder(folder_id)
        if not folder:
            return "Folder does not exist. Please create a folder first.", 404
        
        data = [term, definition, folder_id]
        self.cursor.execute("INSERT INTO flashcards (term, definition, folder_id) VALUES (?,?,?)", data)

        # retrieve the id of the newly created flashcard
        flashcard_id = self.cursor.lastrowid

        # add the flashcard to the folder
        self.folders_db.addFlashcardToFolder(folder_id, flashcard_id)

        # commit the transaction
        self.connection.commit()

    def deleteFlashcard(self, flashcard_id):
        # fetch folder_id
        data = [flashcard_id]
        self.cursor.execute("SELECT folder_id FROM flashcards WHERE id = ?", data)
        folder_id = self.cursor.fetchone()['folder_id']

        # delete the flashcard from the flashcards table
        self.cursor.execute("DELETE FROM flashcards WHERE id = ?", data)

        # remove the flashcard from the flashcards table
        self.folders_db.removeFlashcardFromFolder(folder_id, flashcard_id)
        self.connection.commit()

        return "Flashcard deleted successfully"
    
    def updateFlashcard(self, term, definition, flashcard_id):
        data = [term, definition, flashcard_id]
        self.cursor.execute("UPDATE flashcards SET term = ?, definition = ? WHERE id = ?", data)
        self.connection.commit()