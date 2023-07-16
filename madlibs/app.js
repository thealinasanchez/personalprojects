const URL = "https://code.mollyshewchuk.com/madlibs";
Vue.createApp({
    data() {
        return {
            madlib: {
                words: [],
                id: -1,
            },
            currentIndex: 0,
            answers: [],
            currentPrompt: "",
            completed: false,
            completedMadlib: ""
        }
    },
    methods : {
        savePrompt: function() {
            // if empty bail out
            if (this.currentPrompt == "") return;

            // add current prompt to answers and move on
            this.answers.push(this.currentPrompt)
            this.currentIndex++;
            this.currentPrompt = "";

            if (this.currentIndex == this.madlib.words.length) {
                // stop
                this.completed = true;
                this.generateMadlib();
            }
        },
        generateMadlib: function() {
            var params = new URLSearchParams();
            params.append("id", this.madlib.id);
            params.append("answers", JSON.stringify(this.answers));
            var encodedData = params.toString();
            var requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: encodedData,
            }
            fetch(URL, requestOptions)
            .then(response => response.text())
            .then(data => {
                this.completedMadlib = data;
            })
        }
    },
    created : function() {
        fetch(URL)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            this.madlib.words = data.words;
            this.madlib.id = data.id;
        })
        .catch(error => {
            console.error(error);
        })
    },
    computed: {
        prompt() {
            return this.madlib.words[this.currentIndex];
        }
    }
}).mount("#app");