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

delete a post:
```
    db.delete(post)
    db.commit()
```

remove user:
```
# cascade="all, delete-orphan" deletes all data from the relationship
posts: Mapped[list[Post]] = relationship("Post", back_populates="author", cascade="all, delete-orphan")
```

### Python FastAPI Tutorial (Part 7): Sync vs Async - Converting Your App to Asynchronous

[Python FastAPI Tutorial (Part 7): Sync vs Async - Converting Your App to Asynchronous](https://www.youtube.com/watch?v=2JPDt-Jp6fM)

add depencency for sqlite, a sql driver to handle async operations
```
pip install aiosqlite
or
uv add aiosqlite
```

change all method to be asyncronous:
```
# add keyword 'async' to the begin of method definition
# change Session to AsyncSession
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    # add 'await' to every i/o operation on db
    result = await db.execute(select(models.Post)
                                # add selectinload in every realtion that needs to be load
                              .options(selectinload(models.Post.author))
                              .order_by(models.Post.date_posted.desc()))
```

let fastAPI async handler exception:
```
return await http_exception_handler(request, exception)
```


### Python FastAPI Tutorial (Part 8): Routers - Organizing Routes into Modules with APIRouter

[Python FastAPI Tutorial (Part 8): Routers - Organizing Routes into Modules with APIRouter](https://www.youtube.com/watch?v=NkgIHa6KtHg)

Migrate to routes:
```
from fastapit import APIRouter

router = APIRouter()
```

change app to the router created and remove de '/api/users' path
````
@router.get("", response_model=list[UserResponse])
async def get_users(db: Annotated[AsyncSession, Depends(get_db)]):
```

now add router in main.pi
```
from routers import posts, users

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
```

### Python FastAPI Tutorial (Part 9): Frontend Forms - Connecting JavaScript to Your API

[Python FastAPI Tutorial (Part 9): Frontend Forms - Connecting JavaScript to Your API](https://www.youtube.com/watch?v=vqjZOyT4QRs)

connecting frontend with backend trought javascript and bootstrap modals

### Python FastAPI Tutorial (Part 10): Authentication - Registration and Login with JWT

[Python FastAPI Tutorial (Part 10): Authentication - Registration and Login with JWT](https://www.youtube.com/watch?v=Go4wYJJhR3k)


installing new dependencies:
```
pip install "pwdlib[argon2]" pyjwt pydantic-settings
or
uv add "pwdlib[argon2]" pyjwt pydantic-settings
```

adding a new attribute to the model User:
````
password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
```

updating schemas:
```
password: str = Field(min_length=8)
```

Modifiy UserResponse to UserPublic and UserPrivate:
```
class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    image_file: str | None
    image_path: str

class UserPrivate(UserPublic):
    email: EmailStr
```

create a new Token schema class:
```
class token(BaseModel):
    acces_token: str
    token_type: str
```

create a new file `config.py` on the root of the project:
```
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings() # Loaded from .env file
```

create a .env file:
```
SECRET_KEY=
```

quickly create a secret key on the console:
```
python -c "import secrets; print(secrets.token_hex(32))"
```
outputs something like: `279e7cc0394dee369dc5e6e315ec22ea55033fc0220a842b6830c43eff976eaf`

create an authorization utilities:
```
from datetime import UTC, datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from config import settings

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)
```

### Python FastAPI Tutorial (Part 11): Authorization - Protecting Routes and Verifying Current User

[Python FastAPI Tutorial (Part 11): Authorization - Protecting Routes and Verifying Current User](https://www.youtube.com/watch?v=MY0TFMMm9B0)

Create a dependency and creating an alias to call it:
```
CurrentUser = Annotated[models.User, Depends(get_current_user)]
```

remove hardcode user_id on PostCreate schema.
Add the alias as a parameter on a method router to protected:
```
async def create_post(
    post: PostCreate,
    current_user: CurrentUser, # gets unauthorize if it is not present
    db: Annotated[AsyncSession, Depends(get_db)]
):
```

### Python FastAPI Tutorial (Part 12): File Uploads - Image Processing, Validation, and Storage

[Python FastAPI Tutorial (Part 12): File Uploads - Image Processing, Validation, and Storage](https://www.youtube.com/watch?v=AExumWjfbyo)

add a new dependency to work with images:
```
pip install pillow
or
uv add pillow
```

create a utility class `image_utils.py` to centralize and reuse common image logic

add a maximun size in config.py:
```
max_upload_size_bytes: int = 5 * 1024 * 1024
```

creating in users routes 2 new endpoints:
````
@router.patch("/{user_id}/picture", response_model=UserPrivate)
async def upload_profile_picture(
    user_id: int,
    file: UploadFile,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
...

@router.delete("/{user_id}/picture", response_model=UserPrivate)
async def delete_user_picture(
    user_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
```

