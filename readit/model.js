const mongoose = require("mongoose");
const dotenv = require("dotenv");

dotenv.config();

mongoose.connect(process.env.DB_LINK);


// creating a schema. Sets up for our database
const bookSchema  = new mongoose.Schema({
    title: {
        type: String,
        required:[true, 'Book must have a title.']
    },
    author: {
        type: String,
        required:[true, 'Author must have a name.']
    },
    rating: {
        type: Number,
        required:[true, 'Book must have a rating.']
    }
});

const authorSchema = new mongoose.Schema({
    name: String,
    birthday: Date,
    nationality: String,
    awards: [String]
});

const Book = mongoose.model("Book", bookSchema);
const Author = mongoose.model("Author", authorSchema);

module.exports = {
    Book: Book,
    Author: Author
}