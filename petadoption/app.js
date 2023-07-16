Vue.createApp({
    data() {
      return {
        pets: [],
        search: "",
        filteredPets: [],
        newPet: {
          name: "",
          species: "",
          breed: "",
          age: "",
          gender: "",
        },
        applicants: [],
        modalOpen: false,
        modal: {
          index: -1,
          fullname: "",
          phoneNumber: "",
          email: "",
          petId: ""
        },
        petmodalOpen: false,
        petmodal: {
          index: -1,
          petname:"",
          species: "",
          breed: "",
          age: "",
          gender: ""
        },
        newApplicant: {
          name: "",
          phoneNumber: "",
          email: "",
          petId: "",
        },
        sortOrder: "",
        sortOrderApps: ""
      };
    },
  
    methods: {
      //makes a GET request to the server for all pet listings
      getListings: function () {
        fetch("http://localhost:8080/pets")
          .then((response) => response.json())
          .then((data) => {
            this.pets = data;
            console.log(this.pets);
          });
      },
  
      //makes a POST request to the server from a "create listing" form
      createListing: function () {
        //question: I dont understand headers
        myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/x-www-form-urlencoded");
  
        var encodedData =
          "name=" +
          encodeURIComponent(this.modal.name) +
          "&species=" +
          encodeURIComponent(this.modal.species) +
          "&breed=" +
          encodeURIComponent(this.modal.breed);
        //age: "", gender: "",
        console.log(encodedData);
  
        var requestOptions = {
          method: "POST",
          body: encodedData,
          headers: myHeaders,
        };
  
        fetch("http://localhost:8080/pets", requestOptions).then((response) => {
          if (response.status === 201) {
            response.json().then((data) => {
              this.pets.push(data);
              this.newPet = {};
            });
          } else {
            alert("Not able to add a pet... ");
          }
        });
      },
  
      sortAge: function() {
        console.log(this.sortOrder);
        if (this.sortOrder == 'asc') {
          function compare(a,b) {
            if (a.age > b.age) return -1;
            if (a.age < b.age) return 1;
            return 0;
          }
          this.sortOrder = 'desc';
        }
        else {
          function compare(a,b) {
            if (a.age < b.age) return -1;
            if (a.age > b.age) return 1;
            return 0;
          }
          this.sortOrder = 'asc';
        }
        console.log(this.pets);
        this.pets = this.pets.sort(compare);
      },
  
      sortName: function() {
        console.log(this.sortOrderApps);
        if (this.sortOrderApps == 'asc') {
          function compare(a,b) {
            if (a.name > b.name) return -1;
            if (a.name < b.name) return 1;
            return 0;
          }
          this.sortOrderApps = 'desc';
        }
        else {
          function compare(a,b) {
            if (a.name < b.name) return -1;
            if (a.name > b.name) return 1;
            return 0;
          }
          this.sortOrderApps = 'asc';
        }
        console.log(this.applicants);
        this.applicants.sort(compare);
      },
  
      //makes a DELETE request to the server based on the ID number of the pet being deleted
      deleteListing: function (listingId) {
        var delPet = this.pets[listingId]._id;
        var requestOptions = {
          method: "DELETE",
        };
        fetch(`http://localhost:8080/pets/${delPet}`, requestOptions).then(
          (response) => {
            if (response.status === 204) {
              console.log("pet was deleted");
            } else {
              alert("pet was not deleted");
            }
          }
        );
      },
  
      //makes a GET request for all adoption applications
      getApplications: function () {
        fetch("http://localhost:8080/applications")
          .then((response) => response.json())
          .then((data) => {
            this.applicants = data;
          });
      },
  
      toggleModal: function(index = null) {
        this.modalOpen = !this.modalOpen;
        if (index !== null) {
          let app = this.applicants[index];
          this.modal.index = index;
          this.modal.fullname = fullname;
          this.modal.phoneNumber = phoneNumber;
          this.modal.email = email;
          this.modal.petId = petId;
        }
      },
  
      togglepetModal: function(index = null) {
        this.petmodalOpen = !this.petmodalOpen;
        if (index !== null) {
          let pet = this.pets[index];
          this.petmodal.index = index;
          this.petmodal.petname = petname;
          this.petmodal.species = species;
          this.petmodal.breed = breed;
          this.petmodal.age = age;
          this.petmodal.gender = gender;
        }
      },
  
  
      //makes a POST request to the server from a "new adoption" application form
      createApplication: function () {
        //question: i still don't understand what headers are doing
        myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/x-www-form-urlencoded");
  
        var encodedData =
          "name=" +
          encodeURIComponent(this.newApplicant.name) +
          "&phoneNumber=" +
          encodeURIComponent(this.newApplicant.phoneNumber) +
          "&email=" +
          encodeURIComponent(this.newApplicant.email) +
          "&petId=" +
          encodeURIComponent(this.newApplicant.petId);
  
        var requestOptions = {
          method: "POST",
          body: encodedData,
          headers: myHeaders,
        };
  
        fetch("http://localhost:8080/application", requestOptions).then(
          (response) => {
            if (response.status === 201) {
              response.json().then((data) => {
                this.applicants.push(data);
                this.newApplicant = {};
              });
            } else {
              alert("Did not create new applicant...");
            }
          }
        );
      },
  
      //goes to a different "page" - a.k.a. changes a page data property that hides and shows specific sections
      changePage: function (page) {},
  
      resetSearch: function () {
        this.search = "";
      },
    }, //methods close
  
    created: function () {
      this.getListings();
    }, //created close
  
    watch: {
      search(newSearch, oldSearch) {
        this.filteredPets = this.pets.filter((pet) => {
          return pet.name.toLowerCase().includes(newSearch.toLowerCase());
        });
      },
    },
  
    computed: {},
  }).mount("#app");