# Python FastAPI Tutorial

### (Part 1): Getting Started - Web App + REST API

[Corey Shaffer video](https://www.youtube.com/watch?v=7AMjmCTumuo&t=331s)

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
