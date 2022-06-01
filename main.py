import uvicorn
from api.api_start import app
from dotenv import dotenv_values

CONFIG = dotenv_values('_CI/.env')


if __name__ == '__main__':
    uvicorn.run(app, host=CONFIG['SERVER_HOST'], port=int(CONFIG['SERVER_PORT']), debug=True)
