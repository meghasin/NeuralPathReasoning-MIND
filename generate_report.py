"""
generate_report.py
------------------
Generates a project report PDF for NeuralPathReasoning-MIND.
Output: results/project_report.pdf
"""

from fpdf import FPDF
from pathlib import Path

OUT = Path('/Users/meghamala/projects/NeuralPathReasoning-MIND/results/project_report.pdf')
OUT.parent.mkdir(exist_ok=True)

# ── Colours ──────────────────────────────────────────────────────────────────
DARK_BLUE  = (30,  60, 120)
MID_BLUE   = (52,  90, 160)
LIGHT_BLUE = (220, 230, 245)
WHITE      = (255, 255, 255)
BLACK      = (20,  20,  20)
GREY       = (100, 100, 100)
GREEN_BG   = (214, 245, 214)

class Report(FPDF):
    def header(self):
        pass  # custom header per page via add_page logic

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(*GREY)
        self.cell(0, 10, f'NeuralPathReasoning-MIND  |  Page {self.page_no()}', align='C')

    def cover(self):
        # background bar
        self.set_fill_color(*DARK_BLUE)
        self.rect(0, 0, 210, 80, 'F')
        self.set_fill_color(*MID_BLUE)
        self.rect(0, 80, 210, 8, 'F')

        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 20)
        self.set_xy(15, 20)
        self.multi_cell(180, 10, 'NeuralPathReasoning-MIND', align='C')
        self.set_font('Helvetica', '', 13)
        self.set_xy(15, 42)
        self.multi_cell(180, 8,
            'Neural Bellman-Ford Networks for Drug Repurposing\n'
            'on the MIND Biomedical Knowledge Graph', align='C')
        self.set_font('Helvetica', 'I', 10)
        self.set_xy(15, 66)
        self.cell(180, 6, 'Project Report  -  June 2026', align='C')

        # meta block
        self.set_text_color(*BLACK)
        self.set_fill_color(*LIGHT_BLUE)
        self.rect(15, 95, 180, 38, 'F')
        self.set_font('Helvetica', 'B', 10)
        self.set_xy(20, 99)
        self.cell(50, 7, 'Principal Investigator:')
        self.set_font('Helvetica', '', 10)
        self.set_xy(72, 99)
        self.cell(0, 7, 'Meghamala Sinha, The Scripps Research Institute')

        self.set_font('Helvetica', 'B', 10)
        self.set_xy(20, 108)
        self.cell(50, 7, 'Project:')
        self.set_font('Helvetica', '', 10)
        self.set_xy(72, 108)
        self.cell(0, 7, 'NeuralPathReasoning-MIND (follow-on to WeightedKgBlend)')

        self.set_font('Helvetica', 'B', 10)
        self.set_xy(20, 117)
        self.cell(50, 7, 'Status:')
        self.set_font('Helvetica', '', 10)
        self.set_xy(72, 117)
        self.cell(0, 7, 'Zero-shot evaluation complete; fine-tuning in progress')

        self.set_font('Helvetica', 'B', 10)
        self.set_xy(20, 126)
        self.cell(50, 7, 'Repository:')
        self.set_font('Helvetica', '', 10)
        self.set_xy(72, 126)
        self.cell(0, 7, 'github.com/meghasin/NeuralPathReasoning-MIND')

    def section_title(self, text):
        self.ln(5)
        self.set_fill_color(*DARK_BLUE)
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, f'  {text}', fill=True, ln=True)
        self.set_text_color(*BLACK)
        self.ln(2)

    def subsection(self, text):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*MID_BLUE)
        self.cell(0, 7, text, ln=True)
        self.set_text_color(*BLACK)

    def body(self, text, indent=0):
        self.set_font('Helvetica', '', 10)
        self.set_x(10 + indent)
        self.multi_cell(190 - indent, 5.5, text)
        self.ln(1)

    def bullet(self, text, indent=5):
        self.set_font('Helvetica', '', 10)
        self.set_x(10 + indent)
        self.cell(5, 5.5, chr(149))  # bullet
        self.set_x(10 + indent + 5)
        self.multi_cell(180 - indent, 5.5, text)

    def metric_row(self, label, mrr, h1, h10, highlight=False):
        if highlight:
            self.set_fill_color(*GREEN_BG)
        else:
            self.set_fill_color(248, 248, 248)
        self.set_font('Helvetica', 'B' if highlight else '', 9)
        self.cell(60, 7, label, border=1, fill=True)
        self.set_font('Helvetica', 'B' if highlight else '', 9)
        self.cell(40, 7, mrr, border=1, fill=True, align='C')
        self.cell(40, 7, h1, border=1, fill=True, align='C')
        self.cell(40, 7, h10, border=1, fill=True, align='C')
        self.ln()

    def table_header(self, cols, widths):
        self.set_fill_color(*DARK_BLUE)
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 9)
        for col, w in zip(cols, widths):
            self.cell(w, 7, col, border=1, fill=True, align='C')
        self.ln()
        self.set_text_color(*BLACK)


pdf = Report()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.set_margins(10, 10, 10)

# ── PAGE 1: HEADING + OVERVIEW + ALGORITHM ───────────────────────────────────
pdf.add_page()

# Heading block
pdf.set_fill_color(*DARK_BLUE)
pdf.rect(10, 10, 190, 28, 'F')
pdf.set_text_color(*WHITE)
pdf.set_font('Helvetica', 'B', 15)
pdf.set_xy(10, 14)
pdf.cell(190, 8, 'NeuralPathReasoning-MIND', align='C', ln=True)
pdf.set_font('Helvetica', '', 10)
pdf.set_xy(10, 23)
pdf.cell(190, 7,
    'Neural Bellman-Ford Networks for Drug Repurposing  |  Project Report  -  June 2026',
    align='C')
pdf.set_text_color(*BLACK)
pdf.set_xy(10, 42)
pdf.ln(6)

pdf.section_title('1.  Project Overview')
pdf.body(
    'NeuralPathReasoning-MIND is a follow-on project to WeightedKgBlend, exploring '
    'whether state-of-the-art neural path reasoning methods - specifically the ULTRA '
    'model based on Neural Bellman-Ford Networks (NBFNet) - can dramatically improve '
    'drug repurposing performance on the MIND biomedical knowledge graph.'
)
pdf.body(
    'While WeightedKgBlend achieved its best result with Path-Gated Re-ranking '
    '(MRR = 0.0682), this approach was limited by ProbCBR path coverage (~41%) and '
    'shallow 1-2 hop reasoning. ULTRA applies a generalised Bellman-Ford algorithm '
    'over graph neural networks, learning to propagate and combine relational paths '
    'of arbitrary length in a fully differentiable way - with no task-specific '
    'fine-tuning required.'
)

pdf.section_title('2.  The Algorithm: Neural Bellman-Ford Networks (NBFNet / ULTRA)')
pdf.subsection('2.1  What is NBFNet?')
pdf.body(
    'NBFNet (Zhu et al., NeurIPS 2021) reformulates link prediction as a generalised '
    'Bellman-Ford shortest-path problem on knowledge graphs. For a query (drug, treats, ?), '
    'it computes a "path representation" from the source node (drug) to every candidate '
    'target node (disease) by iteratively aggregating multi-hop relational paths through '
    'the graph using learned message functions.'
)
pdf.body('Key properties of NBFNet:', indent=0)
pdf.bullet('Differentiable: the Bellman-Ford iterations are implemented as graph neural '
           'network layers, making the whole pipeline end-to-end trainable.')
pdf.bullet('Path-aware: unlike TransE/RotatE which score triples independently, NBFNet '
           'explicitly models multi-hop reasoning paths between entities.')
pdf.bullet('Inductive: representations are computed at inference time, allowing '
           'generalisation to unseen entities.')

pdf.ln(2)
pdf.subsection('2.2  What is ULTRA?')
pdf.body(
    'ULTRA (Galkin et al., NeurIPS 2023) extends NBFNet to a universal, transferable '
    'foundation model for knowledge graph reasoning. It is pre-trained on 50 diverse '
    'knowledge graphs simultaneously, learning relation representations that transfer '
    'zero-shot to new graphs - including biomedical KGs like MIND that were never seen '
    'during training.'
)
pdf.body('ULTRA advantages over WeightedKgBlend approaches:', indent=0)
pdf.bullet('Zero-shot transfer: no training on MIND required - ULTRA applies directly.')
pdf.bullet('Arbitrary-depth paths: Bellman-Ford iterations propagate through the full '
           'graph, not limited to 1-2 hop paths like ProbCBR.')
pdf.bullet('All predictions have implicit path support: every score is derived from '
           'relational path aggregation, giving biological interpretability by design.')
pdf.bullet('Pre-trained model: `mgalkin/ultra_50g` available on HuggingFace.')

# ── PAGE 3: WHAT WE DID ───────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title('3.  What We Have Done')

pdf.subsection('3.1  Dataset')
pdf.body(
    'We evaluate on MIND splits_updated - the same updated dataset used in '
    'WeightedKgBlend - comprising 6,761 FDA-approved drug-disease indication edges '
    'across 5 stratified cross-validation folds (676 test / 676 valid / ~5,409 train '
    'per fold). This ensures direct comparability with all WeightedKgBlend baselines.'
)

pdf.subsection('3.2  Zero-Shot ULTRA Inference (Completed)')
pdf.body(
    'We ran ULTRA (ultra_50g, pre-trained on 50 graphs) in zero-shot mode on all 5 '
    'folds of MIND splits_updated using a Kaggle GPU notebook. No fine-tuning was '
    'performed - ULTRA was applied directly to MIND.'
)
pdf.body('Per-fold test results:', indent=0)
pdf.ln(1)

# results table
pdf.table_header(['Fold', 'MRR', 'Hits@1', 'Hits@3', 'Hits@5', 'Hits@10'],
                 [30, 32, 32, 32, 32, 32])
rows = [
    ('Slice 0', '0.3666', '0.2845', '0.3851', '0.4315', '0.4955'),
    ('Slice 1', '0.3469', '0.2704', '0.3676', '0.4168', '0.4955'),
    ('Slice 2', '0.3691', '0.2918', '0.3914', '0.4360', '0.5305'),
    ('Slice 3', '0.3532', '0.2782', '0.3738', '0.4212', '0.4888'),
    ('Slice 4', '0.3486', '0.2870', '0.3716', '0.4085', '0.4917'),
]
for i, (fold, mrr, h1, h3, h5, h10) in enumerate(rows):
    bg = (248, 248, 248) if i % 2 == 0 else (255, 255, 255)
    pdf.set_fill_color(*bg)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(30, 6, fold, border=1, fill=True, align='C')
    pdf.cell(32, 6, mrr, border=1, fill=True, align='C')
    pdf.cell(32, 6, h1, border=1, fill=True, align='C')
    pdf.cell(32, 6, h3, border=1, fill=True, align='C')
    pdf.cell(32, 6, h5, border=1, fill=True, align='C')
    pdf.cell(32, 6, h10, border=1, fill=True, align='C')
    pdf.ln()

# mean row
pdf.set_fill_color(*GREEN_BG)
pdf.set_font('Helvetica', 'B', 9)
pdf.cell(30, 6, 'Mean +/- std', border=1, fill=True, align='C')
pdf.cell(32, 6, '0.3569 +/- 0.009', border=1, fill=True, align='C')
pdf.cell(32, 6, '0.2824 +/- 0.010', border=1, fill=True, align='C')
pdf.cell(32, 6, '0.3779 +/- 0.009', border=1, fill=True, align='C')
pdf.cell(32, 6, '0.4232 +/- 0.009', border=1, fill=True, align='C')
pdf.cell(32, 6, '0.5004 +/- 0.015', border=1, fill=True, align='C')
pdf.ln()

pdf.ln(4)
pdf.subsection('3.3  Comparison to WeightedKgBlend (test set)')
pdf.ln(1)

pdf.table_header(['Method', 'MRR', 'Hits@1', 'Hits@10'], [70, 40, 40, 40])
comp = [
    ('TransE',               '0.0158', '0.0036', '0.0311', False),
    ('ProbCBR',              '0.0138', '0.0050', '0.0296', False),
    ('RotatE',               '0.0460', '0.0135', '0.1100', False),
    ('Simple Ensemble',      '0.0489', '0.0135', '0.1097', False),
    ('Path-Gated Re-ranking','0.0682', '0.0188', '0.1291', False),
    ('ULTRA zero-shot',      '0.3569', '0.2824', '0.5004', True),
]
for label, mrr, h1, h10, hi in comp:
    pdf.metric_row(label, mrr, h1, h10, highlight=hi)

pdf.ln(3)
pdf.body(
    'ULTRA zero-shot outperforms Path-Gated Re-ranking by 5.2x in MRR and 3.9x in '
    'Hits@10. Hits@10 = 0.50 means the correct disease appears in the top-10 '
    'predictions for half of all drug queries, with no training on MIND whatsoever.'
)

# ── PAGE 4: FUTURE PLAN ───────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title('4.  Future Plan')

pdf.subsection('4.1  Fine-Tune ULTRA on MIND (Next Step)')
pdf.body(
    'Zero-shot ULTRA is already a strong baseline. Fine-tuning on MIND splits_updated '
    'is expected to push performance substantially further. The plan:'
)
pdf.bullet('Use ULTRA fine-tuning API (GraFN / ULTRA fine-tune script from the authors) '
           'on Kaggle GPU (P100/T4).')
pdf.bullet('Train for 10-20 epochs on each fold\'s training set (5-fold CV, same splits '
           'as WeightedKgBlend for direct comparison).')
pdf.bullet('Evaluate with filtered MRR / Hits@K on test and valid sets.')
pdf.bullet('Target: MRR > 0.45 (expected gain of ~25-30% over zero-shot based on '
           'reported fine-tuning gains in the ULTRA paper).')

pdf.ln(2)
pdf.subsection('4.2  Mechanistic Path Extraction from NBFNet')
pdf.body(
    'A key advantage of NBFNet over simple KGE methods is that each prediction score '
    'is computed via Bellman-Ford path aggregation - meaning interpretable paths can '
    'be extracted. The plan:'
)
pdf.bullet('Use attention weights from NBFNet\'s final layer to identify the '
           'highest-contributing relational path for each drug-disease prediction.')
pdf.bullet('Extract top-1 mechanistic path for each of the 455 WeightedKgBlend '
           'repurposing candidates and compare to ProbCBR paths.')
pdf.bullet('This provides a richer, deeper mechanistic explanation than ProbCBR\'s '
           '1-2 hop paths, potentially uncovering novel multi-step biological mechanisms.')

pdf.ln(2)
pdf.subsection('4.3  Drug Repurposing Candidate Re-analysis')
pdf.body(
    'Re-run the 455 high-confidence candidate extraction pipeline using ULTRA fine-tuned '
    'predictions instead of Path-Gated predictions:'
)
pdf.bullet('Filter novel drug-disease pairs not in any training/valid/test indication set.')
pdf.bullet('Rank by ULTRA score, extract NBFNet mechanistic paths.')
pdf.bullet('Curate top candidates with biological plausibility assessment.')
pdf.bullet('Compare candidate lists between ULTRA and Path-Gated to identify where '
           'the two methods agree (high-confidence) vs. diverge.')

pdf.ln(2)
pdf.subsection('4.4  Integration with WeightedKgBlend Paper')
pdf.body(
    'Results from this project will feed into a follow-up paper or extended version '
    'of the WeightedKgBlend manuscript:'
)
pdf.bullet('Add ULTRA as a new baseline/method in the results tables.')
pdf.bullet('Position the work as a three-tier progression: '
           'simple KGE -> Path-Gated (hybrid) -> ULTRA (neural path reasoning).')
pdf.bullet('Discuss the trade-off: ULTRA is more powerful but less transparent '
           'than ProbCBR paths; ULTRA + NBFNet path extraction bridges this gap.')

pdf.ln(2)
pdf.subsection('4.5  Longer-Term')
pdf.bullet('Explore NBFNet trained from scratch on MIND (vs. ULTRA transfer).')
pdf.bullet('Investigate inductive setting: predict for drugs/diseases not seen in training.')
pdf.bullet('Extend to multi-relational queries beyond drug-disease indication '
           '(e.g., drug-target, disease-gene).')

# ── PAGE 5: SUMMARY ───────────────────────────────────────────────────────────
pdf.add_page()
pdf.section_title('5.  Summary')

pdf.set_fill_color(*LIGHT_BLUE)
pdf.rect(10, pdf.get_y(), 190, 55, 'F')
y = pdf.get_y() + 4

pdf.set_xy(15, y)
pdf.set_font('Helvetica', 'B', 10)
pdf.cell(0, 6, 'Project: NeuralPathReasoning-MIND', ln=True)

pdf.set_font('Helvetica', '', 10)
items = [
    ('Algorithm',  'ULTRA / NBFNet - Neural Bellman-Ford Networks for KG reasoning'),
    ('Dataset',    'MIND splits_updated - 6,761 indication edges, 5-fold CV'),
    ('Completed',  'Zero-shot ULTRA inference on all 5 folds (MRR = 0.357 +/- 0.009)'),
    ('Key result', '5.2x MRR improvement over Path-Gated Re-ranking, zero training needed'),
    ('Next step',  'Fine-tune ULTRA on MIND + extract NBFNet mechanistic paths'),
    ('Goal',       'New state-of-the-art drug repurposing with interpretable deep paths'),
]
for label, val in items:
    pdf.set_xy(15, pdf.get_y())
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(38, 6, f'{label}:')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, val, ln=True)

pdf.ln(8)
pdf.section_title('6.  References')
refs = [
    '[1] Zhu, Z. et al. (2021). Neural Bellman-Ford Networks: A General Graph Neural '
    'Network Framework for Link Prediction. NeurIPS 2021.',
    '[2] Galkin, M. et al. (2023). Towards Foundation Models for Knowledge Graph '
    'Reasoning. NeurIPS 2023 (ULTRA).',
    '[3] Mayers, M. et al. (2022). A Comprehensive Study of Knowledge Graph-Based '
    'Drug Repurposing. MIND dataset.',
    '[4] Das, R. et al. (2020). Probabilistic Case-Based Reasoning for Open-World '
    'Knowledge Graph Completion. EMNLP 2020.',
    '[5] Sinha, M. et al. (2025). Combining Knowledge Graph Embeddings and Mechanistic '
    'Paths for Drug Repurposing. bioRxiv (WeightedKgBlend).',
]
for ref in refs:
    pdf.set_font('Helvetica', '', 9)
    pdf.set_x(10)
    pdf.multi_cell(190, 5, ref)
    pdf.ln(1)

pdf.output(str(OUT))
print(f'Saved: {OUT}')
