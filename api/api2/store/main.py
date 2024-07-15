from fastapi import FastAPI
from store.routers import api_router

app = FastAPI(title='Store API') # Cria  a aplicação
app.include_router(api_router)   # Adiciona as rotas