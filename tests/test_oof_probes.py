"""Method sanity tests only — not Table II result reproduction."""
import unittest
import numpy as np
from patchshot.oof_probes import best_csi_threshold, query_csi, evaluate_accessibility, evaluate_oof_probe

class OOFProbeTest(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(42)
        x = rng.normal(size=(20, 8, 6)).astype(np.float32)
        y = (x[:,:,0] + .25*x[:,:,1] > 0).astype(np.int8)
        y[[2,5,7,9,11],:] = 0
        self.sx,self.sy,self.qx,self.qy = x[:14],y[:14],x[14:],y[14:]
    def test_threshold(self):
        t, _ = best_csi_threshold(np.array([1,0,0,1]),
                                  np.array([.9,.3,.6,.8]))
        self.assertEqual(t,.8)
        self.assertEqual(query_csi(np.array([1,0,0,1]),
                                   np.array([.9,.3,.6,.8]),t),1.)
    def test_three_probes(self):
        rows,summary = evaluate_accessibility(self.sx,self.sy,self.qx,self.qy,seed=0,folds=4)
        self.assertEqual(len(rows),3)
        self.assertGreaterEqual(summary["EnvelopeCSI"],summary["PrototypeCSI"])
    def test_insufficient_case_strata(self):
        y = self.sy.copy(); y[:,:] = 0
        with self.assertRaises(ValueError):
            evaluate_oof_probe("Prototype",self.sx,y,self.qx,self.qy)

if __name__=="__main__":
    unittest.main()
