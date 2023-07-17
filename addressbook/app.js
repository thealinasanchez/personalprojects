Vue.createApp({
    data() {
      return {
        fullname: "",
        number:0,
        address: "",
        contact: "",
        addresses: [],
      };
    },
    methods: {
      addContact: function () {
        this.addresses.push({
          full_name: this.fullname,
          full_number: this.number,
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