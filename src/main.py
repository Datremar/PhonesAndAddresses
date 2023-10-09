import uvicorn

from fastapi import FastAPI

from config import config
from views.phone_address_view import phone_router


class Main:
    def __init__(self):
        self.app = FastAPI()
        self.app.include_router(phone_router)

    def run(self):
        uvicorn.run(
            app=self.app,
            host=config["server"]["host"],
            port=config["server"]["port"]
        )


if __name__ == "__main__":
    Main().run()
