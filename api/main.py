import uvicorn
from mangum import Mangum
from app.app import app

def main():
    uvicorn.run(app="app:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()

handler = Mangum(app)
