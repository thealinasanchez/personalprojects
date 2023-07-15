Vue.createApp({
    data() {
        return {
            numInput: 0,
            dice: [],

        }
    },
    methods : {
        addDie: function () {
            if (this.numInput > 0) {
                this.dice.push({
                    sides: this.numInput,
                    value: this.numInput,
                });
            }
        },
        rollDie: function(index) {
            let currentDie = this.dice[index];
            let count = 0;
            let rollInterval = setInterval(() => {
                currentDie.value = Math.ceil(Math.random() * currentDie.sides);
                if (count > 20) {
                    clearInterval(rollInterval);
                }
                count ++;
            }, 25);
        },
        rollAllDice: function() {
            for(dieIndex in this.dice) {
                this.rollDie(dieIndex);
            }
        },
        deleteDie: function(index) {
            this.dice.splice(index, 1);
        }
    },
    created : function() {
    }
}).mount("#app");