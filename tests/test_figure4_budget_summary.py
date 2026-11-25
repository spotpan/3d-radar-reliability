"""Numerical consistency of the archived radar-only Figure 4 summaries."""
import unittest
from pathlib import Path
from scripts.plot_verified_figure4 import ROOT, load_verified

class Figure4BudgetSummaryTest(unittest.TestCase):
    def test_aggregates_and_paired_deltas(self):
        a,d=load_verified(ROOT/"reference_results/figure4_verified_budget_summary.csv",
                          ROOT/"reference_results/figure4_verified_paired_deltas_matrix.csv")
        self.assertEqual(len(a),28)
        self.assertEqual(len(d),10)
        self.assertAlmostEqual(a[("heavy_5","PatchShot",.20)][0],.23292830,places=7)
        self.assertAlmostEqual(a[("heavy_10","Frozen prototype",.50)][0],.12089522,places=7)

if __name__=="__main__":unittest.main()
