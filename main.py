from fastapi import FastAPI, HTTPException
import utils
from rcon.source import Client
import uvicorn
import asyncio


app = FastAPI()
config = utils.load_config()
utils.ensure_self_signed_cert()

@app.get("/rcon")
def rcon(command: str, password: str = ""):
    if password != config["password"]:
        raise HTTPException(status_code=500, detail=f"Invalid password")
    else:
        try:
            with Client(config["RconHost"], config["RconPort"], passwd=config["RconPassword"]) as client:
                response = client.run(command)
            return {"status": "success", "response": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка RCON: {str(e)}")



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=config["APIPort"], ssl_certfile="cert.pem", ssl_keyfile="key.pem")