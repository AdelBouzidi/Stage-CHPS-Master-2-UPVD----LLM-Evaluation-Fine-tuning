from pathlib import Path
import re

PROJECT = "/path/to/calypso/workdir/finetuning_domaines_eval"
OLD = "/path/to/calypso/workdir/Phase2_domaines_finetuning"

runs = {
    "A":  ("configs/qwen35-9b-ft-A.yaml",  "data/train_A_chat.jsonl", "prepared/train_A", "outputs/train_A", 2, 2),
    "B":  ("configs/qwen35-9b-ft-B.yaml",  "data/train_B_chat.jsonl", "prepared/train_B", "outputs/train_B", 1, 4),
    "C":  ("configs/qwen35-9b-ft-C.yaml",  "data/train_C_chat.jsonl", "prepared/train_C", "outputs/train_C", 1, 4),

    "AB_antineighbor": ("configs/qwen35-9b-ft-B.yaml", "data/train_A_plus_B_antineighbor_chat.jsonl", "prepared/train_AB_antineighbor", "outputs/train_AB_antineighbor", 1, 4),
    "AC_antineighbor": ("configs/qwen35-9b-ft-C.yaml", "data/train_A_plus_C_antineighbor_chat.jsonl", "prepared/train_AC_antineighbor", "outputs/train_AC_antineighbor", 1, 4),

    "AB_shuffle": ("configs/qwen35-9b-ft-B.yaml", "data/train_A_plus_B_antineighbor_chat.jsonl", "prepared/train_AB_shuffle", "outputs/train_AB_shuffle", 1, 4),
    "AC_shuffle": ("configs/qwen35-9b-ft-C.yaml", "data/train_A_plus_C_antineighbor_chat.jsonl", "prepared/train_AC_shuffle", "outputs/train_AC_shuffle", 1, 4),
}

def source_path(src):
    return Path(OLD) / src

def clean_lines(txt):
    banned = [
        "eval_steps:", "eval_strategy:",
        "save_steps:", "save_strategy:",
        "max_steps:",
        "shuffle_before_merging_datasets:",
        "shuffle_merged_datasets:",
        "evals_per_epoch:",
    ]
    out = []
    for line in txt.splitlines():
        s = line.strip()
        if any(s.startswith(b) for b in banned):
            continue
        out.append(line)
    return "\n".join(out) + "\n"

def replace_dataset_block(txt, dataset_path):
    return re.sub(
        r"datasets:\n\s*-\s*path:\s*.*\n\s*type:\s*chat_template",
        f"datasets:\n  - path: {PROJECT}/{dataset_path}\n    type: chat_template",
        txt,
        flags=re.MULTILINE,
    )

for name, (src, data_path, prepared, output, epochs, evals) in runs.items():
    txt = source_path(src).read_text()
    txt = txt.replace(OLD, PROJECT)

    txt = replace_dataset_block(txt, data_path)
    txt = re.sub(r"dataset_prepared_path: .*", f"dataset_prepared_path: {PROJECT}/{prepared}", txt)
    txt = re.sub(r"output_dir: .*", f"output_dir: {PROJECT}/{output}", txt)
    txt = re.sub(r"num_epochs: .*", f"num_epochs: {epochs}", txt)

    txt = clean_lines(txt)

    txt += f"\nevals_per_epoch: {evals}\n"
    txt += "logging_steps: 1\n"

    if name.endswith("antineighbor"):
        txt += "shuffle_before_merging_datasets: false\n"
        txt += "shuffle_merged_datasets: false\n"

    Path(f"configs/qwen35-9b-ft-{name}.yaml").write_text(txt)

print("Created configs:")
for name in runs:
    print(f"configs/qwen35-9b-ft-{name}.yaml")
