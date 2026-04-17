import sqlite3
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

class Usernames:
    def __init__(self, filename):
        # connect to DB file
        self.connection = sqlite3.connect(filename)
        self.connection.row_factory = dict_factory
        self.folders_db = Folders("folders.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usernames (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                folderlist TEXT
            )
        ''')
    
    def getUsernames(self):
        try:
            self.cursor.execute("SELECT * FROM usernames")
            usernames = self.cursor.fetchall()
            print("Usernames retrieved successfully:", usernames)
            return usernames
        except Exception as e:
            print("An error occurred while retrieving usernames:", str(e))
            return []
    
    def getUsername(self, username_id):
        data = [username_id]
        self.cursor.execute("SELECT * FROM usernames WHERE id = ?", data)
        username = self.cursor.fetchone()
        return username
    
    def createUsername(self, username):
        try:
            folderlist = ""

            data = [username, folderlist]
            self.cursor.execute("INSERT INTO usernames (username, folderlist) VALUES (?,?)", data)
            self.connection.commit()

            return "User created successfully with an empty folder list", 201
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

    def deleteUsername(self, username_id):
        data = [username_id]
        self.cursor.execute("DELETE FROM usernames WHERE id = ?", data)
        self.connection.commit()

    def updateUsername(self, username, folderlist, username_id):
        data = [username, folderlist, username_id]
        self.cursor.execute("UPDATE usernames SET username = ?, folderlist = ? WHERE id = ?", data)
        self.connection.commit()

    def deleteFolderFromFolderlist(self, folder_id):
        data = [folder_id]
        self.cursor.execute("SELECT id FROM usernames WHERE folderlist LIKE ?", data)
        user = self.cursor.fetchone()
        if user:
            user_id = user['id']
            data = [user_id]
            self.cursor.execute("SELECT folderlist FROM usernames WHERE id = ?", data)
            folder_list = self.cursor.fetchone()['folderlist'].split(',')
            if str(folder_id) in folder_list:
                folder_list.remove(str(folder_id))
                new_folderlist = ','.join(folder_list)
                data = [new_folderlist, user_id]
                self.cursor.execute("UPDATE usernames SET folderlist = ? WHERE id = ?", data)
                self.connection.commit()
            else:
                print("Folder not found in user's folderlist.")
        else:
            print("No user found with the folder in their folderlist.")

    def addFolderToFolderlist(self, username_id, folder_id):
        try:
            # get the user by their id
            user = self.getUsername(username_id)

            if user:
                # get the current folderlist of the user
                folder_list = user['folderlist']

                if folder_list:
                    # if flashcardlist IS NOT empty, append the folder ID
                    folder_list += f",{folder_id}"
                else:
                    # if flashcardlist IS empty, set it to the folder ID
                    folder_list = str(folder_id)

                # update the user's flashcardlist in the database
                data = [folder_list, username_id]
                self.cursor.execute("UPDATE usernames SET folderlist = ? where id = ?", data)
                self.connection.commit()
                
                return "Folder added to folderlist successfully", 200
            else:
                return "User not found", 404
        except Exception as e:
            return f"An error occurred with the addFolderToFolderlist: {str(e)}", 500

    
    def getFolderlist(self, username_id):
        try:
            # get the user by their id
            user = self.getUsername(username_id)
            
            if user:
                # extract the folderlist from the user's data
                folderlist = user['folderlist']

                if folderlist:
                    # split the folderlist string into a list of folder IDs
                    folder_ids = folderlist.split(',')
                    return folder_ids
                else:
                    # if the folderlist is empty, return an empty list
                    return []
            
            else:
                return "User not found", 404
        except Exception as e:
            return f"An error occurred with getFolderlist: {str(e)}", 500


