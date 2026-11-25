"""Small correctness checks; do not claim manuscript numerical reproduction."""
import unittest
import numpy as np
from patchshot.data import build_fixed_query_and_support_pool, nested_support_cases
from patchshot.metrics import metric_dict
from patchshot.readout import prototype_scores, choose_threshold

class PatchShotCoreTest(unittest.TestCase):
    def test_split(self):
        q,p = build_fixed_query_and_support_pool(1922, 0)
        s = nested_support_cases(p, 1922, 0.2)
        self.assertEqual((len(q),len(s)), (961,384))
        self.assertFalse(set(q)&set(s))
    def test_prototypes_and_threshold(self):
        support = np.array([[2,0],[1.5,.1],[-2,0],[-1.5,-.1]],dtype=np.float32)
        target = np.array([1,1,0,0],dtype=np.int64)
        a,b = prototype_scores(support,target,support)
        threshold = choose_threshold(a,target,50)
        score = metric_dict(b>=threshold,target,b)
        self.assertGreater(score['CSI'],.9)
        self.assertGreater(score['AP'],.9)
    def test_csi_counts(self):
        r=metric_dict(np.array([1,1,0]),np.array([1,0,1]),np.array([.9,.7,.1]))
        self.assertAlmostEqual(r['CSI'],1/3,places=7)

if __name__ == '__main__':
    unittest.main()
