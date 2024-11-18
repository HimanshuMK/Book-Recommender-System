from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from rapidfuzz import process
import numpy as np
import pickle

# Load the popular books dataframe
popular_df = pickle.load(open('models/popular.pkl', 'rb'))
pt = pickle.load(open('models/pt.pkl', 'rb'))
books = pickle.load(open('models/books.pkl', 'rb'))
similarity_scores = pickle.load(open('models/similarity_scores.pkl', 'rb'))

# Function to get recommended books based on the input
def recommend_book(book_name):
    index = np.where(pt.index == book_name)[0][0]
    # Get similar items (exclude the input book itself)
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))
        data.append(item)

    return data


app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up template rendering
templates = Jinja2Templates(directory="templates")

# Define a route for the homepage
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Create lists of book details to pass to the template
    book_name = list(popular_df['Book-Title'].values)
    author = list(popular_df['Book-Author'].values)
    image = list(popular_df['Image-URL-M'].values)
    votes = list(popular_df['num_ratings'].values)
    rating = list(popular_df['avg_ratings'].values)
    
    # Pass the details to the template in a structured format
    books = [
        {"title": title, "author": auth, "image": img, "votes": vote, "rating": rate}
        for title, auth, img, vote, rate in zip(book_name, author, image, votes, rating)
    ]

    return templates.TemplateResponse("index.html", {"request": request, "books": books})

# Route for the recommendation page
@app.get("/recommend", response_class=HTMLResponse)
async def recommend(request: Request):
    return templates.TemplateResponse("recommend.html", {"request": request})


# Route to handle the recommendation form submission (POST request)
@app.post("/recommend", response_class=HTMLResponse)
async def get_recommendation(request: Request, book_name: str = Form(...)):
    fuzzy_match = False  # Flag to indicate if the book name was corrected
    original_book_name = book_name  # Preserve the user's original input

    if book_name not in pt.index:
        # Use fuzzy matching to find the closest matching book
        result = process.extractOne(book_name, pt.index, score_cutoff=50)

        if result:
            closest_match = result[0]  # The closest matching book title
            book_name = closest_match
            fuzzy_match = True  # Mark that we made a correction

        else:
            # If the book is not found, raise an HTTP exception or display a user-friendly message
            return templates.TemplateResponse(
                "recommend.html", 
                {
                    "request": request,
                    "book_name": book_name,
                    "error_message": "Sorry, we couldn't find any book matching your input. Please try again."
                }
            )
    
    # Get recommended books using the recommend_book function
    recommended_books = recommend_book(book_name)

    # Pass the recommendations to the template
    return templates.TemplateResponse(
        "recommend.html", 
        {
            "request": request,
            "book_name": book_name,
            "recommended_books": recommended_books,
            "fuzzy_match": fuzzy_match,
            "original_book_name": original_book_name
        }
    )

