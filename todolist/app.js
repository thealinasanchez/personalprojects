Vue.createApp({
    data() {
        return {
            modal: {
                description: "",
                category: "",
                index: -1,
            },
            search: "",
            filteredList: [],
            list: [],
            modalOpen: false,
        }
    },
    methods : {
        // creates edit space
        toggleModal: function (index = null) {
            console.log(index);
            this.modalOpen = !this.modalOpen;
            if (index !== null) {
                let item = this.list[index];
                this.modal.index = index;
                this.modal.description = item.description;
                this.modal.category = item.category;
            }
        },

        // adds user edit to list item
        updateList: function() {
            console.log(this.modal.index);
            this.list[this.modal.index].description = this.modal.description;
            this.list[this.modal.index].category = this.modal.category;
        },

        // function for adding to list
        addStuff: function() {
            this.list.push({
                description: this.description,
                category: this.category,
            })
        },

        // function for deleting stuff from list
        deleteStuff: function(item) {
            var index = this.list.indexOf(item);
            this.list.splice(index, 1);
        },
    },
    created : function() {
    },

    watch: {
        search(newSearch, oldSearch) {
            console.log(newSearch);
            this.filteredList = this.list.filter((item) => {
                return item.category.toLowerCase().includes(newSearch.toLowerCase());
            });
        },
    },
}).mount("#app");