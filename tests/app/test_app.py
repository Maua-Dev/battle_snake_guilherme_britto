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

    def test_keeps_heading_when_opponent_is_closer_to_food(self):
        request = self.make_request(food={"x": 6, "y": 3}, opponent_head={"x": 5, "y": 3})

        resp = move(request)

        assert resp["move"] == "right"
        assert resp["shout"] == "Another snake is closer; continuing my path."

    def test_keeps_heading_when_opponent_is_tied(self):
        request = self.make_request(food={"x": 6, "y": 3}, opponent_head={"x": 4, "y": 2})

        resp = move(request)

        assert resp["move"] == "right"
        assert resp["shout"] == "Another snake is closer; continuing my path."

    def test_avoids_wall_when_continuing_heading(self):
        request = self.make_request(food={"x": 4, "y": 2}, opponent_head={"x": 4, "y": 2})
        request["you"]["head"] = {"x": 6, "y": 3}
        request["you"]["body"] = [{"x": 6, "y": 3}, {"x": 5, "y": 3}]

        resp = move(request)

        assert resp["move"] == "up"
        
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