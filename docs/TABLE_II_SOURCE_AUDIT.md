# Table II empirical readout envelope — source audit

The supplied PatchShot OpenReview code archive includes
`legacy/diagnostics/116a_patchshot_probe_accessibility.py`.
The source computes three explicitly evaluated probes:
**Prototype, Linear, k-NN** and their per-split empirical maximum.
The same file includes the original case-grouped out-of-fold (OOF)
support threshold calibration. It is NOT equivalent to selecting
a best method from the final query scores and does not establish
information-theoretic bounds.

The script also depends on
`legacy/diagnostics/113a_patchshot_support_traceability.py`
and original Stage-113 / aligned-environment feature files,
which are not present in the public repository. In particular,
the archive's default representation pairs include several
ERA5-conditioned representations and are not a self-contained
radar-only Table II pipeline. No unvalidated refactoring of
Table II results has been published here.

**Next authentic reproduction step:** connect the code to
verified frozen radar representations and independently trained
support readout outputs, record exact per-seed OOF probe scores,
and verify the paper's H5/H10 envelope, accessibility ratio and
remaining gap from those real records. Do not substitute Table I
support-only CSI or fabricate five-seed data to produce the
Table II numbers.

The original published Table II accessibility ratios reported
in the manuscript are:
- Frozen 3DMAE H5 0.788; H10 0.823.
- Matched CE H5 0.981; H10 0.987.
- PatchShot H5 0.981; H10 0.996.

These numbers are manuscript reference values, *not newly
reproduced independent outputs*.
