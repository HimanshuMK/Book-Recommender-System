// Sample data for book recommendations
const books = [
    {
        title: "To Kill a Mockingbird",
        author: "Harper Lee",
        cover: "https://via.placeholder.com/200x300",
        description: "A novel about the serious issues of race, class, gender, and justice in the American South."
    },
    {
        title: "1984",
        author: "George Orwell",
        cover: "https://via.placeholder.com/200x300",
        description: "A dystopian novel set in a totalitarian society ruled by Big Brother."
    },
    {
        title: "The Great Gatsby",
        author: "F. Scott Fitzgerald",
        cover: "https://via.placeholder.com/200x300",
        description: "A story about the American Dream and the disillusionment of the Jazz Age."
    },
    {
        title: "Pride and Prejudice",
        author: "Jane Austen",
        cover: "https://via.placeholder.com/200x300",
        description: "A classic romance novel that also critiques the British class system."
    }
];

// Function to display book recommendations
function displayBooks() {
    const bookList = document.getElementById("book-list");
    books.forEach(book => {
        const bookCard = document.createElement("div");
        bookCard.className = "book-card";
        
        bookCard.innerHTML = `
            <img src="${book.cover}" alt="${book.title} cover" class="book-cover">
            <h2 class="book-title">${book.title}</h2>
            <p class="book-author">by ${book.author}</p>
            <p class="book-description">${book.description}</p>
        `;
        
        bookList.appendChild(bookCard);
    });
}

// Display the books when the page loads
window.onload = displayBooks;
