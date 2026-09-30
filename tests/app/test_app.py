from src.app.main import read_root, start, move, end

class Test_App:
    def test_read_root(self):
        resp = read_root()

        assert resp == {
            "apiversion": "1",
            "author": "mtlonge43",
            "color": "#084B02",
            "head": "bonhomme",
            "tail": "coffee",
            "version": "1.0.0"
        }
        
    def test_start(self):
        resp = start()

        assert resp == "ok"
        
    def test_move(self):
        resp = move(self.make_request(food={"x": 5, "y": 3}, opponent_head={"x": 0, "y": 0}))

        assert resp["move"] == "right"
        assert resp["shout"] == "Going for the nearest food!"

    @staticmethod
    def make_request(food, opponent_head):
        you = {
            "id": "you",
            "head": {"x": 3, "y": 3},
            "body": [{"x": 3, "y": 3}, {"x": 2, "y": 3}],
        }
        opponent = {
            "id": "opponent",
            "head": opponent_head,
            "body": [opponent_head, {"x": opponent_head["x"], "y": opponent_head["y"] - 1}],
        }
        return {
            "you": you,
            "board": {
                "width": 7,
                "height": 7,
                "food": [food],
                "snakes": [you, opponent],
            },
        }
    
    def test_end(self):
        resp = end()

        assert resp == "ok"