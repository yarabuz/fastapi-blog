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