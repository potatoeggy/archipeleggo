from .config import CONFIG_PORT
from .server import create_app

import uvicorn

def main():
    app = create_app()
    
    
    uvicorn.run(app, host="0.0.0.0", port=CONFIG_PORT)


if __name__ == "__main__":
    main()
