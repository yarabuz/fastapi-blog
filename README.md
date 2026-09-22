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