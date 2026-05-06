from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()



posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]


@app.get("/",include_in_schema=False, response_class=HTMLResponse)
@app.get("/posts",include_in_schema=False, response_class=HTMLResponse)
def home():
    return (
        """
        <html>
            <head>
                <title>FastAPI Blog</title>
            </head>
            <body>
                <h1>Welcome to the FastAPI Blog!</h1>
                <p>Check out our latest posts:</p>
                <ul>
                    <li><a href="/api/posts">View Posts</a></li>
                </ul>
            </body>
        </html>
        """
    )

@app.get("/api/posts")
def get_post():
    return posts