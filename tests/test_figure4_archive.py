import unittest
from tools.audit_figure4_paired_deltas import check

class Figure4ArchiveTest(unittest.TestCase):
    def test_original_seed_arithmetic(self):
        r=check()
        self.assertEqual(len(r),10)
        self.assertAlmostEqual(r[("heavy_5",0)],0.07035186,places=6)
        self.assertAlmostEqual(r[("heavy_10",4)],0.01174989,places=6)

if __name__=="__main__":
    unittest.main()
