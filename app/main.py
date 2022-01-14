from dotenv import load_dotenv
load_dotenv()

import uvicorn

from vars import (
    APP_HOST,
    APP_PORT,
    DEBUG
)

if __name__ == '__main__':
    uvicorn.run('src.app:app', host=APP_HOST, port=APP_PORT, reload=DEBUG)
