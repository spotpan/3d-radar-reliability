"""Objective-matched CE smoke test; skip if Torch is not installed."""
import unittest
import numpy as np

try:
    import torch
except ImportError:
    torch = None

@unittest.skipIf(torch is None, "Torch not installed in light CI")
class MatchedCETest(unittest.TestCase):
    def test_support_only_projection(self):
        from patchshot.matched_ce import train_matched_ce_projection
        x = np.asarray([[2.,0.],[-2.,0.],[1.5,.1],[-1.5,.1]], dtype=np.float32)
        y = np.asarray([1,0,1,0], dtype=np.int64)
        model = train_matched_ce_projection(
            x, y, seed=0, epochs=1, steps_per_epoch=1,
            batch_size=4, device="cpu")
        with torch.no_grad():
            z = model(torch.tensor(x))
        self.assertEqual(tuple(z.shape), (4,128))
        self.assertTrue(bool(torch.isfinite(z).all().item()))

if __name__=="__main__":
    unittest.main()
