# Matched cross-entropy projection control

This is an *objective-matched* supervised adaptation control for the
PatchShot representation-readout question.

The same small projection network, support-only training examples,
balanced support sampling and comparable optimization schedule are used.
The projection is trained with binary cross-entropy through a temporary
classifier. **The temporary classifier is then discarded.** Downstream
scores use the same support-derived positive and negative prototypes
and support-calibrated threshold as the contrastive readout.

This is not interchangeable with a balanced cross-entropy **head** that
is retained for direct classification.

## Run on your own features

```bash
python scripts/run_patchshot.py \
  --npz /path/to/local_frozen_patch_features.npz \
  --mode matched_ce --method "Matched CE" \
  --device cuda --out_dir /path/to/local_output_ce
```

The implementation is in `patchshot/matched_ce.py` and the shared
prototype readout in `patchshot/readout.py`.

No original numerical result tables, seed-specific outputs, trained
weights or underlying radar features are distributed. This is a
research-method release, not an independent numerical reproduction.
