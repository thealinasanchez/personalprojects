Vue.createApp({
    data() {
      return {
        rows: 5,
        columns: 5,
  
        moleRow: -1,
        moleCol: -1,
  
        total: 0,
        score: 0,
      };
    },
    methods: {
      updateMole: function () {
        var updateMoleInt = setInterval(() => {
          this.moleRow = Math.ceil(Math.random() * this.rows);
          this.moleCol = Math.ceil(Math.random() * this.columns);
          this.total++;
          if (this.total >= 10) {
            setTimeout(() => {
              this.moleCol = -1;
              this.moleRow = -1;
            }, 1000);
            clearInterval(updateMoleInt);
          }
        }, 1000);
      },
      hitMole: function () {
        this.score++;
        this.moleRow = -1;
        this.moleCol = -1;
      },
    },
    created: function () {
      // this calls things every time it updatess
      this.updateMole();
    },
  }).mount("#app");