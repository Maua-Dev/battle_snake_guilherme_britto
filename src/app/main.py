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

def seguro_avancar(direcao: str, request: dict, snake: dict, comida: dict | None) -> bool:
    board = request["board"]
    head = snake["head"]
    delta_x, delta_y = DIRECTIONS[direcao]
    next_position = {"x": head["x"] + delta_x, "y": head["y"] + delta_y}

    if not (0 <= next_position["x"] < board["width"]):
        return False
    if not (0 <= next_position["y"] < board["height"]):
        return False

    occupied = [
        segment
        for other_snake in board.get("snakes", [])
        for segment in other_snake.get("body", [])
    ]
    if comida != next_position:
        own_body = snake.get("body", [])
        if own_body:
            occupied.remove(own_body[-1]) if own_body[-1] in occupied else None

    return next_position not in occupied


@app.post("/move")
def move(request: dict):
    board = request.get("board", {})
    snake = request.get("you", {})
    head = snake.get("head")
    foods = board.get("food", [])

    if not head or not foods or "width" not in board or "height" not in board:
        return {"move": direcao_atual(snake), "shout": "Continuing my path."}

    comida_prox = min(foods, key=lambda food: calcular_distancia(head, food))
    distancia = calcular_distancia(head, comida_prox)
    opponents = [
        other
        for other in board.get("snakes", [])
        if other.get("id") != snake.get("id") and other.get("head")
    ]
    opponent_distance = min(
        (calcular_distancia(other["head"], comida_prox) for other in opponents),
        default=float("inf"),
    )

    heading = direcao_atual(snake)
    if distancia < opponent_distance:
        movimentos = sorted(
            DIRECTIONS,
            key=lambda direction: calcular_distancia(
                {
                    "x": head["x"] + DIRECTIONS[direction][0],
                    "y": head["y"] + DIRECTIONS[direction][1],
                },
                comida_prox,
            ),
        )
        melhor_movimento = movimentos
        shout = "Going for the nearest food!"
    else:
        melhor_movimento = [heading] + [
            direction for direction in DIRECTIONS if direction != heading
        ]
        shout = "Another snake is closer; continuing my path."

    selected_move = next(
        (
            direction
            for direction in melhor_movimento
            if seguro_avancar(direction, request, snake, comida_prox)
        ),
        heading,
    )
    return {"move": selected_move, "shout": shout}


@app.post("/end")
def end():
    return "ok"

handler = Mangum(app, lifespan="off")