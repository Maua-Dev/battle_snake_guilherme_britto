import random
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

# GET / - info about the snake (https://docs.battlesnake.com/api/requests/info)
# POST /start - start the game (https://docs.battlesnake.com/api/requests/start)
# POST /move - move the snake (https://docs.battlesnake.com/api/requests/move)
# POST /end - end the game (https://docs.battlesnake.com/api/requests/end)

@app.get("/")
def read_root():
    return {
        "apiversion": "1",
        "author": "mtlonge43",
        "color": "#084B02",
        "head": "bonhomme",
        "tail": "coffee",
        "version": "1.0.0"
    }

@app.post("/start") 
def start():
    return "ok"

DIRECTIONS = {
    "up": (0, 1),
    "down": (0, -1),
    "left": (-1, 0),
    "right": (1, 0),
}


def calcular_distancia(voce: dict, comida: dict) -> int:
    return abs(voce["x"] - comida["x"]) + abs(voce["y"] - comida["y"])

def direcao_atual(snake: dict) -> str:
    body = snake.get("body", [])
    if len(body) < 2:
        return "right"

    head, neck = body[0], body[1]
    delta = (head["x"] - neck["x"], head["y"] - neck["y"])

    for name, vector in DIRECTIONS.items():
        if vector == delta:
            return name
            
    return "right"


@app.post("/move")
def move(request: dict):
    print(request)
    response = {
        "move": "right",
        "shout": "I'm moving right!"
    }
    return response

@app.post("/end")
def end():
    return "ok"

handler = Mangum(app, lifespan="off")