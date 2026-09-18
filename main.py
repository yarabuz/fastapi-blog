from fastapi import FastAPI

app = FastAPI()

@app.get("/")
@app.get("/posts")
def home():
    return "Hello juli :)"

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast",
        "date_posted": "april 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for web development",
        "content": "Python is a great language for web development, and fastAPI makes it even better",
        "date_posted": "april 21, 2025",
	},
]

@app.get("/api/posts")
def get_posts():
    return posts
