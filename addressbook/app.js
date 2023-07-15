Vue.createApp({
    data() {
      return {
        namez: "",
        address: "",
        contact: "",
        addresses: [],
      };
    },
    methods: {
      addContact: function () {
        this.addresses.push({
          full_name: this.namez,
          full_address: this.address,
        });
        console.log(this.addresses);
      },
      deleteContact: function (contact) {
        var index = this.addresses.indexOf(contact);
        this.addresses.splice(index, 1);
      },
    },
    created: function () {},
  }).mount("#app");