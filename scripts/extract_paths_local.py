"""
extract_paths_local.py
----------------------
Finds 2-hop mechanistic paths for ULTRA repurposing candidates using
pandas joins — memory-efficient, no full adjacency dict needed.

For each (drug, disease) pair at rank ≤ PATH_TOP_RANK:
  drug -[r1]-> intermediate -[r2]-> disease

Usage:
    python scripts/extract_paths_local.py
"""

import pandas as pd
import numpy as np
from pathlib import Path

SPLITS_DIR    = Path('/Users/meghamala/projects/WeightedKgBlend/data/splits_updated')
PRED_DIR      = Path('/Users/meghamala/Downloads/ultra_output/predictions/ULTRA')
OUT_PATH      = Path('/Users/meghamala/Downloads/ultra_output/predictions/ULTRA/repurposing_candidates_paths_bfs.tsv')
PATH_TOP_RANK = 5   # only candidates ranked ≤ this
TOP_PATHS     = 3   # max paths to report per pair

def load_kg(slice_dir):
    """Load KGE training triples as a DataFrame."""
    df = pd.read_csv(slice_dir / 'kge_train.tsv', sep='\t',
                     header=None, names=['src', 'rel', 'dst'])
    return df

def load_known(slice_dir):
    known = set()
    for split in ['train', 'test', 'valid']:
        df = pd.read_csv(slice_dir / f'ind_{split}.tsv', sep='\t',
                         header=None, names=['h', 'r', 't'])
        for _, row in df.iterrows():
            known.add((row['h'], row['t']))
    return known

def find_2hop_paths(kg, drug, disease, top_k=TOP_PATHS):
    """
    Find 2-hop paths: drug -[r1]-> X -[r2]-> disease
    Uses pandas join — no adjacency dict needed.
    """
    # hop 1: edges from drug
    h1 = kg[kg['src'] == drug][['rel', 'dst']].rename(
        columns={'rel': 'r1', 'dst': 'mid'})

    if h1.empty:
        return []

    # hop 2: edges into disease
    h2 = kg[kg['dst'] == disease][['src', 'rel']].rename(
        columns={'src': 'mid', 'rel': 'r2'})

    if h2.empty:
        return []

    # join on intermediate node
    merged = h1.merge(h2, on='mid')
    # exclude trivial paths (drug == mid or mid == disease)
    merged = merged[merged['mid'] != drug]
    merged = merged[merged['mid'] != disease]

    if merged.empty:
        return []

    paths = []
    for _, row in merged.head(top_k).iterrows():
        path = f"{drug} -[{row['r1']}]-> {row['mid']} -[{row['r2']}]-> {disease}"
        paths.append(path)

    return paths

all_rows = []

for sl in range(5):
    slice_dir = SPLITS_DIR / f'slice_{sl}'
    pred_path = PRED_DIR / f'slice_{sl}' / 'predictions_test.tsv'

    if not pred_path.exists():
        print(f'slice_{sl}: no predictions, skipping')
        continue

    print(f'slice_{sl}: loading KG...', end=' ', flush=True)
    kg = load_kg(slice_dir)
    known = load_known(slice_dir)
    df_pred = pd.read_csv(pred_path, sep='\t')
    print(f'{len(kg):,} edges, {len(df_pred)} predictions')

    seen = set()
    slice_rows = []

    for _, pred_row in df_pred.iterrows():
        drug = pred_row['drug']
        for k in range(1, PATH_TOP_RANK + 1):
            disease = pred_row.get(f'top{k}_disease', '')
            if not isinstance(disease, str) or not disease:
                continue
            if (drug, disease) in known or (drug, disease) in seen:
                continue
            seen.add((drug, disease))

            paths = find_2hop_paths(kg, drug, disease)

            slice_rows.append({
                'slice':      sl,
                'drug':       drug,
                'disease':    disease,
                'ultra_rank': k,
                'path_1':     paths[0] if len(paths) > 0 else '',
                'path_2':     paths[1] if len(paths) > 1 else '',
                'path_3':     paths[2] if len(paths) > 2 else '',
                'has_path':   len(paths) > 0,
            })

    n_with = sum(r['has_path'] for r in slice_rows)
    print(f'  -> {len(slice_rows)} candidates, {n_with} with 2-hop paths')
    all_rows.extend(slice_rows)

df_out = pd.DataFrame(all_rows)
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df_out.to_csv(OUT_PATH, sep='\t', index=False)

print(f'\nTotal: {len(df_out)} candidates, {df_out["has_path"].sum()} with paths')
print(f'Saved: {OUT_PATH}')

print('\nSample rank-1 candidates with paths:')
sample = df_out[(df_out['ultra_rank'] == 1) & df_out['has_path']][
    ['drug', 'disease', 'path_1']].head(10)
for _, r in sample.iterrows():
    print(f"  {r['drug']} -> {r['disease']}")
    print(f"    {r['path_1']}")
