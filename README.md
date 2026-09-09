# Évaluation et fine-tuning de LLM pour la génération de code Fortran

Ce dépôt contient les principaux éléments expérimentaux réalisés dans le cadre d’un stage de Master 2 CHPS portant sur l’évaluation et le fine-tuning de grands modèles de langage pour la génération de code Fortran.

Le travail porte notamment sur :

- l’évaluation fonctionnelle de programmes Fortran générés par des LLM ;
- la construction et la reconstruction de datasets de fine-tuning ;
- le fine-tuning avec LoRA et QLoRA ;
- l’inférence avec Ollama, OpenWebUI et vLLM ;
- la compilation et l’exécution avec gfortran ;
- l’analyse détaillée des gains, régressions et catégories d’erreurs.

## Benchmark

Le benchmark principal est une adaptation Fortran de HumanEval contenant :

- 164 tâches de programmation ;
- 1 126 tests fonctionnels.

Une solution générée est considérée comme correcte uniquement si elle compile avec succès et passe l’ensemble des tests associés à la tâche.

## Pipelines expérimentaux

### Évaluation initiale des LLM

La première campagne suit le pipeline suivant :

1. sélection d’une tâche du benchmark ;
2. construction du prompt ;
3. génération de code par le LLM ;
4. extraction du code Fortran ;
5. compilation avec gfortran ;
6. exécution sur les tests du benchmark ;
7. comparaison des sorties ;
8. analyse des résultats et des erreurs.

### Fine-tuning de Qwen3.5

Des expériences de fine-tuning LoRA ont été réalisées avec :

- Qwen3.5-9B ;
- Qwen3.5-27B.

Les entraînements ont été configurés avec Axolotl sur une infrastructure HPC, puis les adaptateurs ont été évalués avec vLLM et le pipeline d’évaluation Fortran.

### Expériences Qwen3.6-27B

Une seconde série d’expériences utilise QLoRA avec Qwen3.6-27B.

Les configurations conservées dans ce dépôt couvrent notamment :

- la taille du dataset ;
- la composition du dataset ;
- le learning rate ;
- le nombre d’époques ;
- la température d’inférence ;
- le rang LoRA.

## Datasets de fine-tuning

Trois familles principales de datasets sont incluses :

| Dataset | Nombre d’exemples | Description |
|---|---:|---|
| Type A | 1 676 | Instruction vers programme Fortran correct |
| Type B | 1 474 | Programme erroné et informations d’erreur vers programme corrigé |
| Type C | 1 414 | Programme erroné vers programme corrigé |

Total : **4 564 exemples**.

Les scripts utilisés pour la construction et la reconstruction des datasets sont disponibles dans `datasets/scripts/`.

## Organisation du dépôt

```text
analysis/       Scripts d’analyse et de génération des figures
benchmark/      Benchmark HumanEval Fortran
datasets/       Datasets, statistiques et scripts de construction
evaluation/     Pipelines de génération et d’évaluation fonctionnelle
inference/      Configurations vLLM et Docker pour l’inférence
results/        Résultats expérimentaux consolidés et figures
training/       Configurations Axolotl, Slurm et campagnes de fine-tuning
docs/           Documentation méthodologique et reproductibilité