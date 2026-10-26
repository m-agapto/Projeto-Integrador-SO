import tempfile
import unittest
from pathlib import Path
from app import create_app

class AgendadorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.app = create_app({
            "TESTING": True,
            "DATABASE": str(root / "test.sqlite3"),
            "LOG_DIR": str(root / "logs"),
            "DISABLE_SCHEDULER": True,
            "SECRET_KEY": "test",
        })
        self.client = self.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def test_home_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Central de tarefas", response.data)

    def test_rejects_unauthorized_action(self):
        response = self.client.post("/tasks", data={
            "name": "Teste inválido",
            "action": "rm -rf /",
            "schedule_type": "interval",
            "interval_minutes": "5",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"A", response.data)
        with self.app.app_context():
            from app.database import connect
            with connect(self.app.config["DATABASE"]) as conn:
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0], 0)

if __name__ == "__main__":
    unittest.main()
