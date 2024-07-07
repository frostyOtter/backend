from dotenv import load_dotenv
import pathlib
import os

### load .env file (must be placed in same directory as this file)
wd = pathlib.Path(__file__).parent.resolve()
load_dotenv(dotenv_path=os.path.join(wd,'.env'))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8800,
        reload=True,
        log_level="debug",
    )