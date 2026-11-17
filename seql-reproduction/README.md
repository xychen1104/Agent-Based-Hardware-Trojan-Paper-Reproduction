# SeqL paper reproduction

Xinyue Chen · NYU Tandon

This project reproduces the defensive scan-locking model from Seetal Potluri,
Aydin Aysu, and Akash Kumar, *SeqL: Secure Scan-Locking for IP Protection*,
ISQED 2020. The Python implementation uses the paper's abstract circuit
description and was developed with Codex.

## Run on a CPU

Install Python 3.10 or newer. From the repository root, run:

```bash
python3 run_experiments.py
```

The program regenerates both CSVs under `results/` and prints three PASS
messages. No package installation, GPU, API key, or benchmark download is
required. See [the verified run](results/verification.txt).

## Method

SeqL applies one key gate at functional input (FI) and another at scan
output (SQ). During functional capture, the FI key can alter a stored bit.
The stored bit goes directly to functional Q in SeqL. The SQ key affects
the separate scan path. The EFF-style comparator instead routes the
output mask to functional Q as well.

Cells are indexed from scan-out back toward scan-in. Each scan clock
observes the output of the first cell and shifts the other masked outputs
toward scan-out. The first n clocks unload an n-cell capture. For cell i,
the scan error is the XOR of its FI bit and all effective SQ masks on
its route to scan-out, including its own. The implementation checks that
explicit clocked shifts and this parity calculation agree.

## Experiments and results

| Experiment | Result |
| --- | --- |
| Table I and Figures 2–4 | [All 16 two-cell assignments](results/table_i.csv) match both columns of the published table by row. Four assignments are scan-correct and four are functionally correct. One satisfies both conditions. |
| Theorem 3 | [Exhaustive sweep over 1–8 cells](results/scaling.csv) confirms one jointly correct assignment among 2^n scan-correct assignments in this XOR-chain model. At n=2 the fraction of scan-correct assignments with incorrect functional behavior is 3/4. At n=8 it is 255/256. |
| EFF-style comparison | The same synthetic chains were evaluated with shared output masking. These CSV rows are an additional behavioral comparison. |
| Clocked model and gate polarity | 8,192 cases cover both styles, all three-cell key assignments and polarity combinations, and all three-bit capture words. |

The exhaustive fraction describes the distribution of assignments in the
modeled chain. It does not estimate solver behavior. The implementation
uses independent captures into feed-forward scan cells and omits the
surrounding combinational IP, benchmark-level automation in Section V,
the large-circuit solver studies in Section VI, and physical overhead
measurements. The EFF comparator uses the same two-mask parameterization
as the SeqL model for controlled comparison.

## AI-assisted development

[Agent interaction and validation notes](AI_AGENT_LOG.md) document the
assignment prompt, paper analysis, implementation decisions, and measured
checks. The workflow follows the planning, implementation, and validation
stages described in [LockForge](https://arxiv.org/abs/2511.18531), using a
single Codex session and executable checks. The original LockForge agent
orchestrator was not run.
