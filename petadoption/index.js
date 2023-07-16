const express = require("express");
const cors = require("cors");
const app = express();
const model = require("./model.js"); // NEW SCHEMAS MUST BEGIN WITH "MODEL."
const port = 8080;

app.use(cors());
app.use(express.json());

// CODE BELOW THIS LINE !!!

function petValidator(pet) {
  var errors = [];
  if (!pet.name) {
    errors.push("Pet needs a name");
  }
  if (!pet.species) {
    errors.push("Pet needs an species.");
  }
  if (!pet.breed) {
    errors.push("Pet needs a breed.");
  }
  if (!pet.age) {
    errors.push("Pet needs an age.");
  } else if (isNaN(pet.age)) {
    errors.push("Pet age needs to be a number.");
  }
  if (!pet.gender) {
    errors.push("Pet needs a gender.");
  }
  return errors;
}

function ApplicationValidator(AdoptionApp) {
  var errors = [];
  if (!AdoptionApp.name) {
    errors.push("Application needs a name");
  }
  if (!AdoptionApp.phoneNumber) {
    errors.push("Application needs an phone number");
  } else if (isNaN(AdoptionApp.phoneNumber)) {
    errors.push("Phone Number needs to be a number");
  }
  if (!AdoptionApp.email) {
    errors.push("Application needs an email.");
  }
  if (!AdoptionApp.petId) {
    errors.push("Application needs an ID.");
  } else if (isNaN(AdoptionApp.petId)) {
    errors.push("Pet id needs to be a number");
  }
  return errors;
}

// GET

app.get("/pets", async (req, res) => {
  model.Pet.find().then(function (pets) {
    res.send(pets);
  });
});

app.get("/pets/:petId", async (req, res) => {
  var petID = req.params.petId;
  try {
    const pets = await model.Pet.findOne({ _id: petID });
    res.send(pets);
  } catch (err) {
    res.status(500).send({ error: err.message });
  }
});

app.get("/applications", async (req, res) => {
  try {
    const applications = await model.AdoptionApp.find({});
    res.send(applications);
  } catch (err) {
    res.status(500).send({ error: err.message });
  }
});

app.get("/applications/:applicationId", async (req, res) => {
  var applicationID = req.params.applicationId;
  try {
    const applications = await model.AdoptionApp.find({ _id: applicationID });
    res.send(applications);
  } catch (err) {
    res.status(500).send({ error: err.message });
  }
});

// POST

app.post("/pets", async (req, res) => {
  const newPet = new model.Pet({
    name: req.body.name,
    species: req.body.species,
    breed: req.body.breed,
    age: req.body.age,
    gender: req.body.gender,
  });

  var errors = petValidator(newPet);

  if (errors.length == 0) {
    newPet
      .save()
      .then(function () {
        res.status(201).send(newPet);
      })
      .catch(function (errors) {
        console.log(errors);
        res.status(400).send("Failed to Save Pet");
      });
  } else {
    res.status(422).send(errors);
  }
});

app.post("/applications", async (req, res) => {
  const newApplication = new model.AdoptionApp({
    name: req.body.name,
    phoneNumber: req.body.phoneNumber,
    email: req.body.email,
    petId: req.body.petId,
  });

  var errors = ApplicationValidator(newApplication);
  if (errors.length == 0) {
    newApplication
      .save()
      .then(res.status(201).send("Created Applicaton"))
      .catch(function (errors) {
        res.status(400).send("Failed to save application");
      });
  } else {
    res.status(422).send(errors);
  }
});

// DELETE

app.delete("/pets/:petId", function (req, res) {
  var petID = req.params.petId;

  model.Pet.findOne({ _id: petID })
    .then((pet) => {
      if (pet) {
        model.Pet.deleteOne({ _id: petID }).then((result) => {
          console.log(result.deletedCount);
          res.status(204).send("Pet Deleted.");
        });
      } else {
        res.status(404).send("Pet Not Found.");
      }
    })
    .catch((errors) => {
      console.log(errors);
      res.status(400).send("Pet not found.");
    });
});

app.delete("/applications/:applicationId", function (req, res) {
  var applicationID = req.params.applicationId;

  model.AdoptionApp.findOne({ _id: applicationID })
    .then((application) => {
      if (application) {
        model.AdoptionApp.deleteOne({ _id: applicationID }).then((result) => {
          console.log(result.deletedCount);
          res.status(204).send("Applicaton Deleted.");
        });
      } else {
        res.status(404).send("Application Not Found.");
      }
    })
    .catch((errors) => {
      console.log(errors);
      res.status(400).send("Application not found.");
    });
});

app.listen(port, function () {
  console.log("Server is on port " + port);
});