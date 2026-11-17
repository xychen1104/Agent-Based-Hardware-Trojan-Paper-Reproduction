# AI agent interaction and validation

This is an English development record for the SeqL project.

## User request

Original prompt: “算了，到此为止吧，完成这个作业吧，你给我完成”

The attached assignment requires an AI-assisted reproduction of a selected
paper, source code, results, a README, and documentation of agent
interactions. The user supplied the SeqL paper. The quoted text above is
the actual message accompanying the assignment.

## Paper analysis and implementation

- Codex extracted the paper's text and identified the FI/SQ isolation
  mechanism, the two-cell Table I example, and the scaling result in
  Theorem 3. The model uses the paper's scan-out-first indexing.
- Codex implemented explicit clock-by-clock scan shifting and a separate
  prefix-XOR formula. The Table I assertions check complete sets of
  accepted row IDs for both Boolean columns, so a correct count alone
  cannot pass. In the paper's printed bit order, cell 1 is nearest
  scan-out.
- The scaling experiment compares isolated SeqL output with an
  EFF-style shared output on the same synthetic chains. To exercise
  the implementation beyond the published example, Codex added
  explicit capture-word and gate-polarity checks.
- The local test run passed all checks. GitHub CLI authentication
  checking reported that no host was signed in, so this session prepared
  a repository archive for upload. No simulated log entries were added.

The agent's response is the implementation, README, and recorded results
in this repository. Each result can be regenerated with the README
command.
