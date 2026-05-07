# ULTRA Zero-Shot Results on MIND splits_updated

**Model:** `mgalkin/ultra_50g` (pre-trained on 50 knowledge graphs)
**Setting:** Zero-shot — no fine-tuning on MIND
**Evaluation:** Filtered MRR/Hits@K across 5 stratified folds of `splits_updated`
**Dataset:** MIND `splits_updated` — 6,761 indication edges, 676 test/valid per slice
**Notebook:** `notebooks/kaggle/neuralpathreasoning-ultra-mind.ipynb`

---

## Per-Slice Results

| Slice | Split | MRR    | Hits@1 | Hits@3 | Hits@5 | Hits@10 |
|-------|-------|--------|--------|--------|--------|---------|
| slice_0 | test  | 0.3666 | — | — | — | 0.4955 |
| slice_0 | valid | 0.3789 | — | — | — | 0.5112 |
| slice_1 | test  | 0.3469 | — | — | — | 0.4955 |
| slice_1 | valid | 0.3640 | — | — | — | 0.5097 |
| slice_2 | test  | 0.3691 | — | — | — | 0.5305 |
| slice_2 | valid | 0.3707 | — | — | — | 0.5230 |
| slice_3 | test  | 0.3532 | — | — | — | 0.4888 |
| slice_3 | valid | 0.3590 | — | — | — | 0.5060 |
| slice_4 | test  | 0.3486 | — | — | — | 0.4917 |
| slice_4 | valid | 0.3616 | — | — | — | 0.5104 |

## Summary (mean ± std across 5 slices)

| Split | MRR             | Hits@1          | Hits@3          | Hits@5          | Hits@10         |
|-------|-----------------|-----------------|-----------------|-----------------|-----------------|
| test  | 0.3569 ± 0.0092 | 0.2824 ± 0.0101 | 0.3779 ± 0.0090 | 0.4232 ± 0.0086 | 0.5004 ± 0.0153 |
| valid | 0.3668 ± 0.0072 | 0.2949 ± 0.0103 | 0.3849 ± 0.0128 | 0.4334 ± 0.0122 | 0.5121 ± 0.0058 |

---

## Comparison to WeightedKgBlend Baselines (test set)

| Model                   | MRR    | Hits@1 | Hits@10 | vs ULTRA MRR |
|-------------------------|--------|--------|---------|--------------|
| TransE                  | 0.0158 | 0.0036 | 0.0311  | −95.6%       |
| ProbCBR                 | 0.0138 | 0.0050 | 0.0296  | −96.1%       |
| RotatE                  | 0.0460 | 0.0135 | 0.1100  | −87.1%       |
| Simple Ensemble         | 0.0489 | 0.0135 | 0.1097  | −86.3%       |
| Path-Gated (best)       | 0.0682 | 0.0188 | 0.1291  | −80.9%       |
| **ULTRA zero-shot**     | **0.3569** | **0.2824** | **0.5004** | — |

**ULTRA zero-shot outperforms Path-Gated by 5.2× in MRR and 3.9× in Hits@10.**

Key observations:
- **No fine-tuning** — ULTRA transfers directly from 50 pre-training graphs to MIND without seeing any indication edges
- **Hits@10 = 0.50** — the correct disease is in the top-10 predictions for half of all drug queries
- **Hits@1 = 0.28** — the correct disease is the top prediction 28% of the time
- Consistent across slices (low std): MRR std = 0.0092, confirming robustness
