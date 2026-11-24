"""Unit tests on small hand-constructed inputs; NOT study results."""
import unittest
from tools.audit_instability import summarize


def row(case, patch, draw, score, target, mode="drop_low", boundary=""):
    return {"case_id": case, "patch_id": patch, "perturbation": mode,
            "draw_id": str(draw), "event_score": str(score),
            "reference_event": str(target), "is_boundary": boundary}


class TestEventInstability(unittest.TestCase):
    def test_vote_and_u(self):
        rows = [row("a", "0", 1, .2, 1, boundary="1"),
                row("a", "0", 2, .8, 1, boundary="1"),
                row("a", "1", 1, .1, 0), row("a", "1", 2, .2, 0)]
        r = summarize(rows, .5, 2)[0]
        self.assertEqual((r["tp"], r["fp"], r["fn"]), (1, 0, 0))
        self.assertEqual(r["f1"], 1.0)
        self.assertEqual(r["mean_u"], .5)
        self.assertEqual(r["boundary_u"], 1.0)

    def test_duplicate_draw_rejected(self):
        rows = [row("a", "0", 1, .2, 1), row("a", "0", 1, .8, 1)]
        with self.assertRaises(ValueError):
            summarize(rows, .5, 2)

    def test_missing_draw_rejected(self):
        with self.assertRaises(ValueError):
            summarize([row("a", "0", 1, .2, 1)], .5, 2)

    def test_no_model_outputs_is_not_reproduction(self):
        with self.assertRaises(ValueError):
            summarize([], .5, 2)


if __name__ == "__main__":
    unittest.main()
