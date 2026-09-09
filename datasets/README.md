# Fortran fine-tuning datasets

This directory contains the three dataset families used during the
Qwen3.5 fine-tuning experiments.

## Dataset families

| File | Type | Number of examples |
|---|---|---:|
| `final/type_a_final.json` | Instruction → correct Fortran program | 1,676 |
| `final/type_b_final.json` | Erroneous program + error information → corrected program | 1,474 |
| `final/type_c_final.json` | Erroneous program → corrected program | 1,414 |

Total: **4,564 examples**.

The combined `fortran_abc_full.json` file is not duplicated in this
repository because it corresponds to the aggregation of the three
families above.

Dataset construction and reconstruction scripts are available under
`datasets/scripts/`.

The `stats/` directory contains statistics generated during dataset
construction.

## Provenance

The datasets were produced during the CERFACS internship experiments
from collected and reconstructed Fortran code, followed by filtering,
compilation/execution checks and dataset-specific transformations.

See the repository documentation for methodology and provenance details.
