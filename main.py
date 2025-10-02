import asyncio
import sys

from fastapi import FastAPI

from contextlib import asynccontextmanager

from database import create_tables
from router import router as posts_router


app = FastAPI()
app.include_router(posts_router)

if len(sys.argv) > 1:
    if sys.argv[1] == 'migrate':
        asyncio.run(create_tables())
