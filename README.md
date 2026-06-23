# NeuralPathReasoning-MIND

Neural path reasoning for drug repurposing on the MIND biomedical knowledge graph using **ULTRA** (Neural Bellman-Ford Networks).

This project is a follow-on to [WeightedKgBlend](https://github.com/meghasin/WeightedKgBlend), exploring whether state-of-the-art neural path reasoning can dramatically outperform traditional KGE ensemble methods for drug-disease link prediction.

---

## Background

[WeightedKgBlend](https://github.com/meghasin/WeightedKgBlend) achieved its best result with Path-Gated Re-ranking (MRR = 0.068), but was limited by:
- Shallow 1-2 hop ProbCBR path coverage (~41%)
- No end-to-end differentiable path reasoning

**ULTRA** ([Galkin et al., NeurIPS 2023](https://arxiv.org/abs/2310.04562)) is a universal, transferable foundation model for knowledge graph reasoning built on **NBFNet** (Neural Bellman-Ford Networks). It is pre-trained on 50 diverse knowledge graphs and transfers zero-shot to new graphs, including biomedical KGs never seen during training.

### Why NBFNet / Bellman-Ford?

NBFNet ([Zhu et al., NeurIPS 2021](https://arxiv.org/abs/2106.06935)) reformulates link prediction as a generalised Bellman-Ford shortest-path problem. For a query `(drug, treats, ?)`, it iteratively propagates and aggregates multi-hop relational paths through the graph via learned message functions — fully differentiable, arbitrary depth, and path-aware by design.

---

## Dataset

**MIND `splits_updated`** — the updated version of the Mechanistic Repositioning Network (MRN):
- 6,761 FDA-approved drug-disease indication edges (5,370 original + 1,391 new from DrugCentral)
- 250,035 nodes, 9,652,116 edges, 9 node types, 22 relation types
- 5-fold stratified cross-validation: 676 test / 676 valid / ~5,409 train per fold

Available on Zenodo: [https://zenodo.org/records/20184623](https://zenodo.org/records/20184623)

---

## Results

### Zero-Shot ULTRA (Completed)

ULTRA (`ultra_50g`, pre-trained on 50 graphs) applied directly to MIND with **no fine-tuning**.

| Fold | MRR | Hits@1 | Hits@3 | Hits@5 | Hits@10 |
|------|-----|--------|--------|--------|---------|
| slice_0 | 0.3666 | 0.2845 | 0.3851 | 0.4315 | 0.4955 |
| slice_1 | 0.3469 | 0.2704 | 0.3676 | 0.4168 | 0.4955 |
| slice_2 | 0.3691 | 0.2918 | 0.3914 | 0.4360 | 0.5305 |
| slice_3 | 0.3532 | 0.2782 | 0.3738 | 0.4212 | 0.4888 |
| slice_4 | 0.3486 | 0.2870 | 0.3716 | 0.4085 | 0.4917 |
| **Mean +/- std** | **0.3569 +/- 0.009** | **0.2824 +/- 0.010** | **0.3779 +/- 0.009** | **0.4232 +/- 0.009** | **0.5004 +/- 0.015** |

### Comparison to WeightedKgBlend (test set)

| Method | MRR | Hits@1 | Hits@10 |
|--------|-----|--------|---------|
| TransE | 0.0158 | 0.0036 | 0.0311 |
| ProbCBR | 0.0138 | 0.0050 | 0.0296 |
| RotatE | 0.0460 | 0.0135 | 0.1100 |
| Simple Ensemble | 0.0489 | 0.0135 | 0.1097 |
| Path-Gated Re-ranking | 0.0682 | 0.0188 | 0.1291 |
| **ULTRA zero-shot** | **0.3569** | **0.2824** | **0.5004** |

ULTRA zero-shot outperforms Path-Gated Re-ranking by **5.2x in MRR** and **3.9x in Hits@10** with no training on MIND.

### Fine-Tuned ULTRA (In Progress)

Fine-tuning `ultra_50g` on each fold's training indication edges. Target: MRR > 0.45.

---

## Repository Structure

```
NeuralPathReasoning-MIND/
├── notebooks/
│   └── kaggle/
│       ├── neuralpathreasoning-ultra-mind.ipynb   # Zero-shot inference + path extraction
│       ├── kernel-metadata.json                   # Kaggle push config (zero-shot)
│       ├── ultra-finetune-mind.ipynb              # Fine-tuning notebook
│       └── finetune-kernel-metadata.json          # Kaggle push config (fine-tuning)
├── scripts/
│   └── extract_paths_local.py                     # 2-hop BFS path extraction (local)
├── results/
│   ├── ultra_results.md                           # Zero-shot results summary
│   └── project_report.pdf                         # Full project report
└── generate_report.py                             # Generates project_report.pdf
```

---

## Notebooks

### 1. Zero-Shot Inference (`neuralpathreasoning-ultra-mind.ipynb`)

Runs ULTRA `ultra_50g` in zero-shot mode across all 5 folds of MIND `splits_updated` on Kaggle GPU.

**Output:** `predictions_test.tsv` and `predictions_valid.tsv` per slice, plus `repurposing_candidates_paths.tsv`.

**Pipeline:**
1. Install PyTorch 2.2.2+cu118 + PyG (P100/T4/A100 compatible)
2. Load ULTRA checkpoint (`ultra_50g.pth` bundled in ULTRA repo)
3. Build PyG graph from KGE training triples for each fold
4. Score all candidate diseases for every drug query using ULTRA's NBFNet forward pass
5. Filtered evaluation (MRR, Hits@1/3/5/10) — known true triples excluded from ranking
6. Extract 2/3-hop mechanistic paths via BFS for repurposing candidates

### 2. Fine-Tuning (`ultra-finetune-mind.ipynb`)

Fine-tunes `ultra_50g` on each fold's training indication edges using self-adversarial negative sampling loss.

**Strategy:**
- Freeze the relation encoder (preserves generalisation from pre-training on 50 graphs)
- Fine-tune the entity encoder only
- 15 epochs per fold, LR = 1e-4, 32 negative samples per positive triple
- Save best checkpoint per fold by validation MRR

---

## Running on Kaggle

### Zero-shot notebook
```bash
cd notebooks/kaggle
kaggle kernels push -p . --metadata kernel-metadata.json
```

### Fine-tuning notebook
```bash
cd notebooks/kaggle
kaggle kernels push -p . --metadata finetune-kernel-metadata.json
```

The `splits_updated` dataset is available as `megha90/wkb-splits-updated` on Kaggle.

---

## Local Path Extraction

After downloading predictions from Kaggle:

```bash
# Edit PRED_DIR in the script to point to your downloaded predictions
python scripts/extract_paths_local.py
```

Finds 2-hop mechanistic paths of the form:
```
drug -[inhibits]-> gene -[associated_with]-> disease
```
for all novel drug-disease candidates ranked <= 5 by ULTRA.

---

## Future Work

1. **Fine-tuned ULTRA evaluation** — expected MRR > 0.45 (~25-30% gain over zero-shot)
2. **NBFNet path extraction** — use attention weights from NBFNet layers to identify the highest-contributing relational paths per prediction
3. **Drug repurposing candidate re-analysis** — re-run the 455-candidate pipeline from WeightedKgBlend using ULTRA fine-tuned predictions
4. **Integration with WeightedKgBlend paper** — add ULTRA as a new method in the results tables

---

## References

- Zhu, Z. et al. (2021). [Neural Bellman-Ford Networks: A General Graph Neural Network Framework for Link Prediction.](https://arxiv.org/abs/2106.06935) NeurIPS 2021.
- Galkin, M. et al. (2023). [Towards Foundation Models for Knowledge Graph Reasoning.](https://arxiv.org/abs/2310.04562) NeurIPS 2023.
- Mayers, M. et al. (2022). A Comprehensive Study of Knowledge Graph-Based Drug Repurposing. MIND dataset.
- Das, R. et al. (2020). Probabilistic Case-Based Reasoning for Open-World Knowledge Graph Completion. EMNLP 2020.
- Sinha, M. et al. (2025). Combining Knowledge Graph Embeddings and Mechanistic Paths for Drug Repurposing. bioRxiv. [WeightedKgBlend](https://github.com/meghasin/WeightedKgBlend)
