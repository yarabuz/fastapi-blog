# Python FastAPI Tutorial

### (Part 1): Getting Started - Web App + REST API

[Python FastAPI Tutorial(Part 1): Getting Started - Web App + REST API](https://www.youtube.com/watch?v=7AMjmCTumuo&t=331s)

using UV: [documentation](https://docs.astral.sh/uv/#installation)

Creating a uv project:
```
uv init fastapi_blog
```

enter to the created foder
```
cd fastapi_blog
```

add with uv fastapi as a dependency with the standard package:
```
uv add "fastapi[standard]"
```
to define and endpoint, in a new file:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello juli :)"}
```

to run the app:
```
uv run fastapi dev main.py
```

application running on:
[http://localhost:8000/](http://localhost:8000/)

you should get:
```
{"message":"Hello juli :)"}
```

check the documentation site:
[http://localhost:8000/docs](http://localhost:8000/docs)

and its new version:
[http://localhost:8000/redoc](http://localhost:8000/redoc)


### (Part 2): HTML Frontend for Your API - Jinja2 Templates

[Python FastAPI Tutorial (Part 2): HTML Frontend for Your API - Jinja2 Templates](https://www.youtube.com/watch?v=G4NIB9Rx9Qs)

not necessary if you install fastapi[standard]
```
pip install jinja2
or
uv add jinja
```

define a template variables pointing to a new folder with the templates:
```
templates = Jinja2Templates(directory="templates")
```

now html pages should return:
```
def home(request: Request):
    return templates.TemplateResponse(request, "home.html")
```

passing variable to the template in the third parameter as a dictionary:
```
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts})
```
then using with curly braces and percentage simbols:
```
    {% for post in posts %}
        <div>
            <h2>{{ post.title }}</h2>
            <p>{{ post.content }}</p>
        </div>
    {% endfor %}
```

setting a static folder:
```
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

### Python FastAPI Tutorial (Part 3): Path Parameters - Validation and Error Handling

[Python FastAPI Tutorial (Part 3): Path Parameters - Validation and Error Handling](https://www.youtube.com/watch?v=WRjXIA5pMtk)

add curly braces with a name, a that same name in the signature of the method with a type
```
@app.get("/api/post/{post_id}")
def get_post(post_id: int)
```

To return a 404 error code:

```
from fastapi import HTTPException, status
```

raise an excpetion with a few arguments
```
raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
```

using curly braces with url_for to redirect a method name and parameters
```
<a class="article-title" href="{{ url_for('post_page', post_id=post.id) }}">{{ post.title }}</a>
```

Handling errors:
```
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail if exception.detail else "An error ocurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code
    )
```

Handling error for validations errors:
```
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
    )
```

### Python FastAPI Tutorial (Part 4): Pydantic Schemas - Request and Response Validation

[Python FastAPI Tutorial (Part 4): Pydantic Schemas - Request and Response Validation](https://www.youtube.com/watch?v=9GHxnttXxrA)

Adding schemas for validations in the docs:
```
from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
```
```
@app.get("/api/posts", response_model=list[PostResponse])
def get_posts():
    return posts
```

New endpoint for creating a post:
```
@app.post("/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    new_id = max(post["id"] for post in posts) + 1 if posts else 1 # handling incremental id
    new_post = {
        "id": new_id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "date_posted": "September 22, 2026"
    }
    posts.append(new_post)
    return new_post
```

### Python FastAPI Tutorial (Part 5): Adding a Database - SQLAlchemy Models and Relationships

[Python FastAPI Tutorial (Part 5): Adding a Database - SQLAlchemy Models and Relationships](https://www.youtube.com/watch?v=NvOV3ig2tGY)

Install SQLAlchemy:
```
pip install sqlalchemy
or
uv add sqlalchemy
```

creating a new file for database config:
```
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db" # url connection

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(declarative_base):
    pass

def get_db():
    with SessionLocal() as db:
        yield db
```

creating models, example:
```
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)

    posts: Mapped[list[Post]] = relationship("Post", back_populates="author")
```

### Python FastAPI Tutorial (Part 6): Completing CRUD - Update and Delete (PUT, PATCH, DELETE)

[Python FastAPI Tutorial (Part 6): Completing CRUD - Update and Delete (PUT, PATCH, DELETE)](https://www.youtube.com/watch?v=VyoGAoxQhxM)

creating a new optional schema:
```
class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_lenght=1, max_length=100)
    content: str | None = Field(Default=None, min_length=1)
```

Patch method to partially update sent fields:
```
# exclude None values
update_data = post_data.model_dump(exclude_unset=True)
# updating each field
for field, value in update_data.items():
    setattr(post, field, value)
```