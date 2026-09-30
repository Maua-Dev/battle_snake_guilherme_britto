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
        
    def test_end(self):
        resp = end()

        assert resp == "ok"