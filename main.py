import fastapi

app = fastapi.FastAPI()

@app.get('/')
async def home():
    return "home page"

@app.get('/info')
async def info():
    return "info page"

