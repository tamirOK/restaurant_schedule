import fastapi

from . import endpoints


app = fastapi.FastAPI(
    title='Restaurant schedule API',
    openapi_url='/openapi.json',
    version='0.0.1',
)
app.include_router(endpoints.router)
