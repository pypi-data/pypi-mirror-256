# Sleekify
A minimalistic, ASGI Python framework for building REST API's. Heavily inspired by Express.js and FastAPI.

Installation:
```
pip install sleekfiy
```

Usage:
```
from sleekfiy import App

app = App()

app.post("/")
async def endpoint(name: str):
  return { "name": name }
```
  
