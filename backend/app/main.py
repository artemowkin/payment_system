from fastapi import FastAPI

from .project.db import engine, Base, init_commands

from .users.routes import router as users_router
from .merchants.routes import router as merchants_router
from .transactions.routes import router as transactions_router


app = FastAPI(docs_url='/api/docs/', redoc_url='/api/redoc/', openapi_url='/api/openapi.json')

app.include_router(users_router, prefix='/api/auth', tags=['users'])

app.include_router(merchants_router, prefix='/api/merchants', tags=['merchants'])

app.include_router(transactions_router, prefix='/api/transactions', tags=['transactions'])


@app.on_event('startup')
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await init_commands.execute_commands()


@app.on_event('shutdown')
async def on_shutdown():
    await engine.dispose()
