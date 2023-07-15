Vue.createApp({
    data() {
      return {
        message: "",
        messageBank: [
          "Yes",
          "No",
          "Maybe",
          "Ask Again Tomorrow",
          "Probably",
          "Probably Not",
        ],
        question: "",
        history: [],
      };
    },
    methods: {
      askQuestion: function () {
        if (!this.isValidQuestion()) return;
  
        let index = Math.floor(Math.random() * this.messageBank.length);
        this.message = this.messageBank[index];
  
        this.history.push({
          question: this.question,
          answer: this.message,
        });
  
        console.log(this.history);
  
        this.question = "";
      },
      isValidQuestion: function () {
        return this.question[this.question.length - 1] == "?";
      },
      deleteItem: function (item) {
        var index = this.history.indexOf(item);
        this.history.splice(index, 1);
      },
    },
  }).mount("#app");