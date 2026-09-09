# Qwen27 detailed failure analysis — corrected strict version

Results dir: `qwen27/epoch1/learning_rate_1/results`
Reference run: `A`
Runs detected: **15**
Tasks detected: **164**

Validation: details OK counts match summary OK counts.

## 1. Model ranking and failure categories

| run_name | family | ok | failures | compile_error | wrong_output | runtime_error | timeout | unknown_failure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | baseline_ft_A | 62 | 102 | 54 | 9 | 39 | 0 | 0 |
| ABC_filtered_accept_C | filtered_accept_subset | 56 | 108 | 69 | 10 | 29 | 0 | 0 |
| ABC_filtered_accept_A | filtered_accept_subset | 55 | 109 | 79 | 8 | 22 | 0 | 0 |
| AB_antineighbor | baseline_ft_AB | 55 | 109 | 72 | 10 | 27 | 0 | 0 |
| ABC_filtered_reject | filtered_reject | 54 | 110 | 75 | 11 | 24 | 0 | 0 |
| ABC_filtered_accept | filtered_accept_all | 53 | 111 | 70 | 13 | 27 | 0 | 0 |
| ABC_filtered_manual | filtered_manual | 53 | 111 | 72 | 16 | 23 | 0 | 0 |
| ABC_source_numericalhub | source_subset | 52 | 112 | 78 | 10 | 24 | 0 | 0 |
| ABC_filtered_accept_AC_shuffle | filtered_accept_subset | 48 | 116 | 59 | 19 | 36 | 0 | 0 |
| ABC_source_burkardt | source_subset | 48 | 116 | 81 | 13 | 21 | 0 | 0 |
| ABC_source_fortran_lang | source_subset | 46 | 118 | 82 | 12 | 24 | 0 | 0 |
| ABC_filtered_accept_AB_shuffle | filtered_accept_subset | 41 | 123 | 66 | 36 | 21 | 0 | 0 |
| ABC_filtered_accept_B | filtered_accept_subset | 41 | 123 | 86 | 10 | 27 | 0 | 0 |
| ABC_filtered_accept_BC_shuffle | filtered_accept_subset | 39 | 125 | 83 | 13 | 28 | 0 | 0 |
| ABC_dedup_BC | abc_dedup_bc | 32 | 132 | 36 | 76 | 20 | 0 | 0 |

## 2. Pairwise comparison vs FT-A

| run_name | run_ok | delta_vs_ref | both_ok | run_only_unique_wins | ref_only_losses | both_fail |
| --- | --- | --- | --- | --- | --- | --- |
| A | 62 | 0 | 62 | 0 | 0 | 102 |
| ABC_filtered_accept_C | 56 | -6 | 42 | 14 | 20 | 88 |
| ABC_filtered_accept_A | 55 | -7 | 37 | 18 | 25 | 84 |
| AB_antineighbor | 55 | -7 | 42 | 13 | 20 | 89 |
| ABC_filtered_reject | 54 | -8 | 40 | 14 | 22 | 88 |
| ABC_filtered_accept | 53 | -9 | 38 | 15 | 24 | 87 |
| ABC_filtered_manual | 53 | -9 | 39 | 14 | 23 | 88 |
| ABC_source_numericalhub | 52 | -10 | 36 | 16 | 26 | 86 |
| ABC_filtered_accept_AC_shuffle | 48 | -14 | 32 | 16 | 30 | 86 |
| ABC_source_burkardt | 48 | -14 | 35 | 13 | 27 | 89 |
| ABC_source_fortran_lang | 46 | -16 | 34 | 12 | 28 | 90 |
| ABC_filtered_accept_AB_shuffle | 41 | -21 | 26 | 15 | 36 | 87 |
| ABC_filtered_accept_B | 41 | -21 | 33 | 8 | 29 | 94 |
| ABC_filtered_accept_BC_shuffle | 39 | -23 | 26 | 13 | 36 | 89 |
| ABC_dedup_BC | 32 | -30 | 22 | 10 | 40 | 92 |

## 3. Hardest tasks

| task_id | success_count | dominant_failure | ok_runs |
| --- | --- | --- | --- |
| 1 | 0 | compile_error |  |
| 3 | 0 | runtime_error |  |
| 7 | 0 | runtime_error |  |
| 10 | 0 | compile_error |  |
| 14 | 0 | runtime_error |  |
| 16 | 0 | runtime_error |  |
| 17 | 0 | compile_error |  |
| 19 | 0 | compile_error |  |
| 22 | 0 | runtime_error |  |
| 23 | 0 | runtime_error |  |
| 27 | 0 | runtime_error |  |
| 28 | 0 | runtime_error |  |
| 29 | 0 | runtime_error |  |
| 30 | 0 | runtime_error |  |
| 33 | 0 | compile_error |  |
| 37 | 0 | wrong_output |  |
| 42 | 0 | runtime_error |  |
| 48 | 0 | runtime_error |  |
| 51 | 0 | compile_error |  |
| 58 | 0 | compile_error |  |
| 66 | 0 | runtime_error |  |
| 74 | 0 | compile_error |  |
| 78 | 0 | runtime_error |  |
| 81 | 0 | compile_error |  |
| 82 | 0 | runtime_error |  |
| 84 | 0 | compile_error |  |
| 86 | 0 | compile_error |  |
| 87 | 0 | compile_error |  |
| 92 | 0 | wrong_output |  |
| 95 | 0 | compile_error |  |
