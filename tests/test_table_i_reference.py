"""Check archived Table I rows without requiring Torch or radar data."""
import unittest
from tools.audit_table_i_reference import audit

class ArchivedTableITest(unittest.TestCase):
    def test_archived_five_seed_values(self):
        rows = audit()
        self.assertEqual(len(rows), 6)
        names = {name for name, _, _, _ in rows}
        self.assertEqual(names, {"Raw-MAE","SupConShot","Matched CE re-access"})

if __name__=="__main__":
    unittest.main()
