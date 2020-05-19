#!/usr/bin/env python3

from pathlib import Path

from dotenv import load_dotenv

from binday.server.factories.application import create_application

app = create_application()

if __name__ == "__main__":
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path, verbose=True)

    app.run()
