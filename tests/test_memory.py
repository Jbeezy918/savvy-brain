import tempfile,unittest
from pathlib import Path
import core.storage as storage
import core.memory as memory
class ScopeTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();storage.DB_PATH=Path(self.tmp.name)/"test.db";storage.initialize()
 def tearDown(self):self.tmp.cleanup()
 def test_isolation(self):
  memory.remember("project:alpha","alpha-only");memory.remember("project:beta","beta-only");self.assertEqual([x["content"] for x in memory.recall("project:alpha")],["alpha-only"]);self.assertFalse(memory.recall("project:beta","alpha-only"))
 def test_master_isolation(self):
  memory.remember("project:alpha","private");memory.remember("master","summary");self.assertEqual([x["content"] for x in memory.recall("master")],["summary"])
 def test_message_scope(self):
  storage.add_message("s","user","hello","alpha");self.assertEqual(storage.rows("SELECT scope_id FROM messages")[0]["scope_id"],"project:alpha")
if __name__=="__main__":unittest.main()
