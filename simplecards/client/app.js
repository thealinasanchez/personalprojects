console.log("connected");

// global variable to store current userId
var userId;

// global variable to store current folderId
var folderId;

// creating simple cards wrapper
var simpleCardsWrapper = document.getElementById("wrapper");

// nav bar
var navbar = document.getElementById("navbar");

// logout button
var logoutButton = document.createElement("div");
logoutButton.id = "logout-button";
logoutButton.className = "button";
logoutButton.innerHTML = "Logout";
navbar.appendChild(logoutButton);
logoutButton.addEventListener("click", handleLogout);

// create folder button
var createFolderButton = document.createElement("div");
createFolderButton.id = "create-folder-button";
createFolderButton.className = "button";
createFolderButton.innerHTML = "Create Folder";
navbar.appendChild(createFolderButton);
createFolderButton.addEventListener("click", createFolder);

document.addEventListener("DOMContentLoaded", function() {
    // create overlay when the page loads
    createLoginSignupOverlay();
});

function createLoginSignupOverlay() {
    // ##### LOGIN DIV STUFF #####

    // create overlay div
    var overlayDiv = document.createElement("div");
    overlayDiv.id = "overlay";
    document.body.appendChild(overlayDiv);

    // login div
    var loginDiv = document.createElement("div");
    loginDiv.id = "login-div";
    overlayDiv.appendChild(loginDiv);

    // username text
    var usernameText = document.createElement("p");
    usernameText.id = "username-text";
    usernameText.innerHTML = "Username: ";
    loginDiv.appendChild(usernameText);

    // username input
    var usernameInput = document.createElement("input");
    usernameInput.id = "username-input";
    usernameInput.type = "text";
    usernameInput.placeholder = "ex: jane_doe";
    loginDiv.appendChild(usernameInput);

    // login button
    var loginButton = document.createElement("div");
    loginButton.id = "login-button";
    loginButton.className = "button";
    loginButton.innerHTML = "Login";
    loginDiv.appendChild(loginButton);

    // signup text to go to signup div
    var signupTextToggle = document.createElement("p");
    signupTextToggle.id = "signup-text-toggle";
    signupTextToggle.innerHTML = "Don't have an account? Sign up here";
    loginDiv.appendChild(signupTextToggle);

    // ##### SIGN UP DIV STUFF #####

    // signup div
    var signupDiv = document.createElement("div");
    signupDiv.id = "signup-div";
    signupDiv.style.display = "none";
    overlayDiv.appendChild(signupDiv);

    // signup text
    var signupText = document.createElement("p");
    signupText.id = "signup-text";
    signupText.innerHTML = "Create a Username: ";
    signupDiv.appendChild(signupText);

    // signup input
    var signupInput = document.createElement("input");
    signupInput.id = "signup-input";
    signupInput.type = "text";
    signupInput.placeholder = "Ex: jane_doe";
    signupDiv.appendChild(signupInput);

    // signup button
    var signupButton = document.createElement("div");
    signupButton.id = "signup-button";
    signupButton.className = "button";
    signupButton.innerHTML = "Sign Up";
    signupDiv.appendChild(signupButton);

    // login text to go to login div
    var loginTextToggle = document.createElement("p");
    loginTextToggle.id = "login-text-toggle";
    loginTextToggle.innerHTML = "Already have an account? Log in here";
    signupDiv.appendChild(loginTextToggle);

    // #### TOGGLE CLICKING EVENTS ####

    // signup text click event
    signupTextToggle.onclick = function() {
        loginDiv.style.display = "none";
        signupDiv.style.display = "block";
    }

    loginTextToggle.onclick = function() {
        loginDiv.style.display = "block";
        signupDiv.style.display = "none";
    }

    loginButton.addEventListener("click", handleLogin);
    signupButton.addEventListener("click", handleSignup);
}

function handleLogin() {
    // get username input value
    var username = document.getElementById("username-input").value;

    // fetch list of usernames
    fetch("http://localhost:8080/usernames")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(usernames => {
            var userExists = usernames.some(user => user.username === username);
            if (userExists) {
                // extract user id from user object
                userId = usernames.find(user => user.username === username).id;

                // hide login/signup divs & overlay
                document.getElementById("login-div").style.display = "none";
                document.getElementById("signup-div").style.display = "none";
                document.getElementById("overlay").style.display = "none";
                loadFoldersFromServer();
            } else {
                alert("Username not found. Please sign up or try again.");
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            alert("An error occurred while fetching data. Please try again later.");
        });
}

function handleSignup() {
    // get username input value
    var usernameInput = document.getElementById("signup-input");
    var username = usernameInput.value.trim();
    var data = "username=" + encodeURIComponent(username);
    
    console.log("Data to be sent to server:", data);

    // send POST request to create username
    fetch("http://localhost:8080/usernames", {
        method:"POST",
        body: data,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to create username");
        }
        return response.json();
    })
    .then(user => {
        userId = user.id;

        document.getElementById("login-div").style.display = "none";
        document.getElementById("signup-div").style.display = "none";
        document.getElementById("overlay").style.display = "none";
    })
    .catch(error => {
        console.error("Error handling signup:", error);
        alert("An error occurred during signup. Please try again later.");
    });
}

function handleLogout() {
    simpleCardsWrapper.innerHTML = "";
    document.getElementById("login-div").style.display = "block";
    document.getElementById("signup-div").style.display = "none";
    document.getElementById("overlay").style.display = "block";
    document.getElementById("signup-input").value = "";
    document.getElementById("username-input").value = "";
}

function generateFolders(folderData) {
    // folder div
    var folderDiv = document.createElement("div");
    folderDiv.className = "folder";
    folderDiv.id = "folder-" + folderData.id;
    console.log("Generated folder ID:", folderDiv.id)
    simpleCardsWrapper.appendChild(folderDiv);

    // button div
    var buttonDiv = document.createElement("div");
    buttonDiv.className = "button-div";
    folderDiv.appendChild(buttonDiv);

    // folder name
    var folderName = document.createElement("h1");
    folderName.className = "folder-name";
    folderName.innerHTML = folderData.folder_name;
    folderDiv.appendChild(folderName);

    // folder creator
    var folderCreator = document.createElement("h3");
    folderCreator.className = "folder-creator";
    folderCreator.innerHTML = "Created by: " + folderData.creator;
    folderDiv.appendChild(folderCreator);

    // png folder edit icon
    var folderEditIcon = document.createElement("img");
    folderEditIcon.src = "icons/edit.png";
    folderEditIcon.alt = "Edit icon";
    folderEditIcon.className = "icon folder-edit-icon";
    buttonDiv.appendChild(folderEditIcon);

    // png folder delete icon
    var folderDeleteIcon = document.createElement("img");
    folderDeleteIcon.src = "icons/trash.png";
    folderDeleteIcon.alt = "Delete icon";
    folderDeleteIcon.className = "icon folder-delete-icon";
    buttonDiv.appendChild(folderDeleteIcon);

    // folder create flashcards button
    var createFlashcardsButton = document.createElement("div");
    createFlashcardsButton.className = "button create-flashcards-button";
    createFlashcardsButton.innerHTML = "Create flashcards";
    folderDiv.appendChild(createFlashcardsButton);

    // folder arrow
    var folderArrow = document.createElement("img");
    folderArrow.src = "icons/down-arrow.png";
    folderArrow.alt = "arrow icon";
    folderArrow.className = "folder-arrow";
    folderDiv.appendChild(folderArrow);

    // flashcard container
    var flashcardContainer = document.createElement("div");
    flashcardContainer.className = "flashcard-container";
    folderDiv.appendChild(flashcardContainer);

    // edit folder click
    folderEditIcon.addEventListener("click", function(event) {
        event.stopPropagation();
        editFolder(folderData.id);
    });

    // delete folder click
    folderDeleteIcon.addEventListener("click", function(event) {
        event.stopPropagation();
        deleteFolder(folderData.id);
    });

    // create flashcards click
    createFlashcardsButton.addEventListener("click", function(event) {
        event.stopPropagation();
        createFlashcard(folderData.id);
    })

    // folder click toggles flashcards
    folderDiv.addEventListener("click", function() {
        if (flashcardContainer.innerHTML.trim() === "") {
            loadFlashcardsFromServer(folderData.id, flashcardContainer);
            folderArrow.src = "icons/up-arrow.png";
        } else {
            flashcardContainer.innerHTML = "";
            folderArrow.src = "icons/down-arrow.png";
        }
    });
}

function loadFoldersFromServer() {
    // send GET request to fetch folders associated with current user
    fetch(`http://localhost:8080/usernames/${userId}/folders`)
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then(folders => {
        simpleCardsWrapper.innerHTML = "";

        // fetch folders for each folder ID associated with the user
        folders.forEach(folderData => {
            generateFolders(folderData);
        });
    })
    .catch(error => {
        console.error("Error loading folders:", error);
        alert("An error occurred while loading folders. Please try again later.");
    });
}

function createFolder() {
    // show overlay, hide login div & signup div
    document.getElementById("overlay").style.display = "block";
    document.getElementById("login-div").style.display = "none";
    document.getElementById("signup-div").style.display = "none";

    // create folder div
    var createFolderDiv = document.createElement("div");
    createFolderDiv.id = "create-folder-div";
    document.getElementById("overlay").appendChild(createFolderDiv);

    // create folder folder_name input
    var folderNameInput = document.createElement("input");
    folderNameInput.type = "text";
    folderNameInput.id = "folder-name-input";
    folderNameInput.placeholder = "Ex: Biology Ch. 1"
    createFolderDiv.appendChild(folderNameInput);

    // create folder button
    var createFolderButton = document.createElement("div");
    createFolderButton.id = "create-folder-button";
    createFolderButton.className = "button";
    createFolderButton.innerHTML = "Create";
    createFolderDiv.appendChild(createFolderButton);

    // event listener for create folder button
    createFolderButton.addEventListener("click", function() {
        var folderName = folderNameInput.value;
        var data = "folder_name=" + encodeURIComponent(folderName)
                    + "&creator_id=" + encodeURIComponent(userId);
        console.log("Data to be sent to server", data);

        fetch("http://localhost:8080/folders", {
            method: "POST",
            body: data,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
        .then(function(response) {
            console.log("New folder created", response);

            // clear input field
            folderNameInput.value = "";

            // close overlay after folder creation
            document.getElementById("overlay").style.display = "none";
            createFolderDiv.style.display = "none";

            // refresh folder display
            loadFoldersFromServer();
        })
        .catch(function(error) {
            console.error("Error creating folder:", error);
            alert("An error occurred while creating the folder. Please try again later.");
        });
    });
}

function editFolder(folderId) {
    // show overlay, hide everything else
    document.getElementById("overlay").style.display = "block";

    // create edit folder div
    var editFolderDiv = document.createElement("div");
    editFolderDiv.id = "edit-folder-div";
    document.getElementById("overlay").appendChild(editFolderDiv);

    // create folder name input
    var folderNameInput = document.createElement("input");
    folderNameInput.type = "text";
    folderNameInput.id = "edit-folder-name-input";
    folderNameInput.placeholder = "Ex: Cool New Folder";
    editFolderDiv.appendChild(folderNameInput);

    // create save button
    var saveButton = document.createElement("div");
    saveButton.id = "save-button";
    saveButton.className = "button";
    saveButton.innerHTML = "Save";
    editFolderDiv.appendChild(saveButton);

    // create cancel button
    var cancelButton = document.createElement("div");
    cancelButton.id = "cancel-button";
    cancelButton.className = "button";
    cancelButton.innerHTML = "Cancel";
    editFolderDiv.appendChild(cancelButton);

    // event listener for save button
    saveButton.addEventListener("click", function() {
        var newFolderName = folderNameInput.value;

        // send PUT request to update folder name
        var data = "folder_name=" + encodeURIComponent(newFolderName);
        fetch(`http://localhost:8080/folders/${folderId}`, {
            method: "PUT",
            body: data,
            headers: {
                "Content-Type":"application/x-www-form-urlencoded"
            }
        })
        .then(function(response) {
            if(!response.ok) {
                throw new Error("Failed to update folder name");
            }
            console.log("Folder name updated successfully", response);

            // close overlay after saving
            document.getElementById("overlay").style.display = "none";
            editFolderDiv.style.display = "none";

            // refresh folder display
            loadFoldersFromServer();
        })
        .catch(function(error) {
            console.error("Error updating folder name:", error);
            alert("An error occurred while updating the folder name. Please try again later.");
        });
    });

    // event listener for cancel button
    cancelButton.addEventListener("click", function() {
        // close overlay without saving
        document.getElementById("overlay").style.display = "none";
        editFolderDiv.style.display = "none";
    })
}


function deleteFolder(folderId) {
    // confirm with user before deleting folder
    var confirmDelete = confirm("Are you sure you want to delete this folder?");
    if (confirmDelete) {
        // send DELETE request to the server to delete the folder
        fetch(`http://localhost:8080/folders/${folderId}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
        .then(function(response) {
            if(!response.ok) {
                throw new Error("Failed to delete folder");
            }
            console.log("Folder deleted successfully", response);

            // remove folder from UI
            var folderToRemove = document.getElementById(`folder-${folderId}`);
            if (folderToRemove) {
                folderToRemove.remove();
            }
        })
        .catch(function(error) {
            console.error("Error deleting folder:", error);
            alert("An error occurred while deleting the folder. Please try again later,");
        });
    }
}

function generateFlashcards(flashcardData, flashcardContainer) {
    var flashcardDiv = document.createElement("div");
    flashcardDiv.className = "flashcard";
    flashcardDiv.id = `flashcard-${flashcardData.id}`;

    if (flashcardData && flashcardData.term !== undefined && flashcardData.definition !== undefined) {

        // term
        var termDiv = document.createElement("div");
        termDiv.className = "flashcard-term";
        termDiv.textContent = "Term: " + flashcardData.term;
        flashcardDiv.appendChild(termDiv);

        // definition
        var definitionDiv = document.createElement("div");
        definitionDiv.className = "flashcard-definition";
        definitionDiv.textContent = "Definition: " + flashcardData.definition;
        flashcardDiv.appendChild(definitionDiv);

        // edit button
        var flashcardEditButton = document.createElement("div");
        flashcardEditButton.id = "flashcard-edit-button";
        flashcardEditButton.className = "button";
        flashcardEditButton.textContent = "Edit";
        flashcardDiv.appendChild(flashcardEditButton);

        // delete button
        var flashcardDeleteButton = document.createElement("div");
        flashcardDeleteButton.id = "flashcard-delete-button";
        flashcardDeleteButton.className = "button";
        flashcardDeleteButton.textContent = "Delete";
        flashcardDiv.appendChild(flashcardDeleteButton);

        // event listener for delete button
        flashcardDeleteButton.addEventListener("click", function(event) {
            event.stopPropagation();
            deleteFlashcard(flashcardData.id);
        });

        // event listener for edit button
        flashcardEditButton.addEventListener("click", function(event) {
            event.stopPropagation();
            editFlashcard(flashcardData);
        })
    } else {
        return;
    }   
    flashcardContainer.appendChild(flashcardDiv);
}

function loadFlashcardsFromServer(folderId, flashcardContainer) {
    fetch(`http://localhost:8080/folders/${folderId}/flashcards`)
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then(flashcards => {
        // clear the flashcard container
        flashcardContainer.innerHTML = "";

        if (flashcards && Array.isArray(flashcards) && flashcards.length > 0) {
            flashcards.forEach(flashcard => {
                generateFlashcards(flashcard, flashcardContainer);
            });
        } else {
            console.log("No flashcards found for this folder.");
        }
    })
    .catch(error => {
        console.error("Error loading flashcards:", error);
        alert("An error occurred while loading flashcards. Please try again later.");
    });
}

function createFlashcard(folderId) {
    // show overlay, hide login div & signup div
    document.getElementById("overlay").style.display = "block";
    document.getElementById("login-div").style.display = "none";
    document.getElementById("signup-div").style.display = "none";

    // create flashcard div
    var createFlashcardDiv = document.createElement("div");
    createFlashcardDiv.id = "create-flashcard-div";
    document.getElementById("overlay").appendChild(createFlashcardDiv);

    // create flashcard term input
    var flashcardTermInput = document.createElement("input");
    flashcardTermInput.type = "text";
    flashcardTermInput.id = "flashcard-term-input";
    flashcardTermInput.placeholder = "Ex: Mitochondria";
    createFlashcardDiv.appendChild(flashcardTermInput);

    // create flashcard definition input
    var flashcardDefinitionInput = document.createElement("input");
    flashcardDefinitionInput.type = "text";
    flashcardDefinitionInput.id = "flashcard-definition-input";
    flashcardDefinitionInput.placeholder = "Ex: Powerhouse of the cell";
    createFlashcardDiv.appendChild(flashcardDefinitionInput);

    // create flashcard button
    var createFlashcardButton = document.createElement("div");
    createFlashcardButton.id = "create-flashcard-button";
    createFlashcardButton.className = "button";
    createFlashcardButton.innerHTML = "Create";
    createFlashcardDiv.appendChild(createFlashcardButton);

    // create flashcard cancel button
    var createFlashcardCancelButton = document.createElement("div");
    createFlashcardCancelButton.id = "create-flashcard-cancel-button";
    createFlashcardCancelButton.className = "button";
    createFlashcardCancelButton.innerHTML = "Cancel";
    createFlashcardDiv.appendChild(createFlashcardCancelButton);

    // event listener for cancel create flashcard button
    createFlashcardCancelButton.addEventListener("click", function(event) {
        event.stopPropagation();

        flashcardDefinitionInput.value = "";
        flashcardTermInput.value = "";
        createFlashcardDiv.style.display = "none";
        document.getElementById("overlay").style.display = "none";

    })

    // event listener for create flashcard button
    createFlashcardButton.addEventListener("click", function(event) {
        event.stopPropagation();

        var term = flashcardTermInput.value;
        var definition = flashcardDefinitionInput.value;
        var data = "term=" + encodeURIComponent(term)
                    + "&definition=" + encodeURIComponent(definition)
                    + "&folder_id=" + encodeURIComponent(folderId);
        console.log("Data to be sent to the server", data);

        fetch("http://localhost:8080/flashcards", {
            method: "POST",
            body: data,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
        .then(function(response) {
            console.log("New flashcard created", response);

            // clear input field
            flashcardDefinitionInput.value = "";
            flashcardTermInput.value = "";

            // close overlay after flashcard creation
            document.getElementById("overlay").style.display = "none";
            createFlashcardDiv.style.display = "none";

            // refresh flashcard display
            loadFlashcardsFromServer(folderId, document.getElementById(`folder-${folderId}`).querySelector(".flashcard-container"));
        })
        .catch(function(error) {
            console.error("Error creating flashcard:", error);
            alert("An error occurred while creating the flashcard. Please try again later.");
        });
    });
}

function deleteFlashcard(flashcardId) {
    var confirmDelete = confirm("Are you sure you want to delete this flashcard?");
    if (confirmDelete) {
        // send DELETE request to the server to delete the flashcard
        fetch(`http://localhost:8080/flashcards/${flashcardId}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
        .then(function(response) {
            if (!response.ok) {
                throw new Error("Failed to delete flashcard");
            }
            console.log("Flashcard deleted successfully", response);

            // remove flashcard from UI if deletion is successful
            var flashcardToRemove = document.getElementById(`flashcard-${flashcardId}`);
            if (flashcardToRemove) {
                flashcardToRemove.remove();
            }
        })
        .catch(function(error) {
            console.error("Error deleting flashcard:", error);
            alert("An error occurred while deleting the flashcard. Please try again later.");
        });
    }
}

function editFlashcard(flashcardData) {
    // show overlay, hide everything else
    document.getElementById("overlay").style.display = "block";

    // edit flashcard div
    var editFlashcardDiv = document.createElement("div");
    editFlashcardDiv.id = "edit-flashcard-div";
    document.getElementById("overlay").appendChild(editFlashcardDiv);

    // edit term input
    var editTermInput = document.createElement("input");
    editTermInput.type = "text";
    editTermInput.id = "edit-term-input";
    editTermInput.placeholder = "Enter term";
    editTermInput.value = flashcardData.term;
    editFlashcardDiv.appendChild(editTermInput);

    // edit definition input
    var editDefinitionInput = document.createElement("input");
    editDefinitionInput.type = "text";
    editDefinitionInput.id = "edit-definition-input";
    editDefinitionInput.placeholder = "Enter definition";
    editDefinitionInput.value = flashcardData.definition;
    editFlashcardDiv.appendChild(editDefinitionInput);

    // save button
    var editSaveButton = document.createElement("div");
    editSaveButton.id = "edit-save-button";
    editSaveButton.className = "button";
    editSaveButton.innerHTML = "Save";
    editFlashcardDiv.appendChild(editSaveButton);

    // cancel button
    var editCancelButton = document.createElement("div");
    editCancelButton.id = "edit-cancel-button";
    editCancelButton.className = "button";
    editCancelButton.innerHTML = "Cancel";
    editFlashcardDiv.appendChild(editCancelButton);

    // event listener for save button
    editSaveButton.addEventListener("click", function (event) {
        event.stopPropagation();

        var newTerm = editTermInput.value;
        var newDefinition = editDefinitionInput.value;

        var data = "term=" + encodeURIComponent(newTerm) 
                    + "&definition=" + encodeURIComponent(newDefinition);
        
        fetch(`http://localhost:8080/flashcards/${flashcardData.id}`, {
            method: "PUT",
            body: data,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
        .then(function(response) {
            if (!response.ok) {
                throw new Error("Failed to update flashcard");
            }
            console.log("Flashcard updated successfully", response);

            // close overlay after saving
            document.getElementById("overlay").style.display = "none";
            editFlashcardDiv.style.display = "none";

            // refresh flashcard display
            loadFlashcardsFromServer(flashcardData.folder_id, document.getElementById(`folder-${flashcardData.folder_id}`).querySelector(".flashcard-container"));
        })
        .catch(function(error) {
            console.error("Error updating flashcard:", error);
            alert("An error occurred while updating the flashcard. Please try again later.");
        });
    });

    // event listener for cancel button
    editCancelButton.addEventListener("click", function(event) {
        event.stopPropagation();
        document.getElementById("overlay").style.display = "none";
        editFlashcardDiv.style.display = "none";
    });
}