import uvicorn
from api.api_start import app


if __name__ == '__main__':
    uvicorn.run(app, host='192.168.0.23', port=8000)
