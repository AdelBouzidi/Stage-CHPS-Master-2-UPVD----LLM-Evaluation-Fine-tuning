# Évaluation et fine-tuning de LLM pour la génération de code Fortran

Ce dépôt regroupe les principaux éléments expérimentaux réalisés pendant un stage de Master 2 CHPS consacré à l’évaluation et au fine-tuning de grands modèles de langage pour la génération de code Fortran.

Le travail porte principalement sur :

- l’évaluation de programmes Fortran générés par des LLM ;
- la construction et l’amélioration de datasets pour le fine-tuning ;
- le fine-tuning avec LoRA et QLoRA ;
- l’inférence avec Ollama, OpenWebUI et vLLM ;
- la compilation et l’exécution des programmes avec gfortran ;
- l’analyse des résultats, des gains, des régressions et des erreurs.

## Benchmark

Le benchmark principal est une version Fortran de HumanEval. Il contient :

- 164 tâches de programmation ;
- 1 126 tests fonctionnels.

Une solution est considérée comme correcte uniquement si le programme compile et passe tous les tests associés à la tâche.

## Pipelines expérimentaux

### Évaluation initiale des LLM

La première campagne d’évaluation suit les étapes suivantes :

1. sélection d’une tâche du benchmark ;
2. construction du prompt ;
3. génération d’une réponse par le LLM ;
4. extraction du code Fortran ;
5. compilation avec gfortran ;
6. exécution du programme sur les tests du benchmark ;
7. comparaison des résultats obtenus avec les résultats attendus ;
8. analyse du résultat final et des erreurs éventuelles.

### Fine-tuning de Qwen3.5

Des expériences de fine-tuning avec LoRA ont été réalisées sur deux modèles :

- Qwen3.5-9B ;
- Qwen3.5-27B.

Les entraînements ont été réalisés avec Axolotl sur une infrastructure HPC.

Les adaptateurs obtenus ont ensuite été chargés avec vLLM afin de générer les solutions Fortran et de les évaluer avec le même pipeline fonctionnel.

### Expériences Qwen3.6-27B

Une autre série d’expériences a été réalisée avec Qwen3.6-27B en utilisant QLoRA.

Plusieurs paramètres ont été étudiés, notamment :

- la taille du dataset ;
- le type de dataset utilisé ;
- le learning rate ;
- le nombre d’époques ;
- la température utilisée pendant l’inférence ;
- le rang LoRA.

## Datasets de fine-tuning

Trois types principaux de datasets sont présents dans ce dépôt :

| Dataset | Nombre d’exemples | Description |
|---|---:|---|
| Type A | 1 676 | Une instruction associée à un programme Fortran correct |
| Type B | 1 474 | Un programme incorrect avec des informations sur l’erreur, associé à sa correction |
| Type C | 1 414 | Un programme incorrect associé à sa version corrigée |

Au total, ces trois datasets contiennent **4 564 exemples**.

Les scripts utilisés pour construire et améliorer ces datasets sont disponibles dans :

`datasets/scripts/`

## Organisation du dépôt

```text
analysis/       Scripts d’analyse et de génération des figures
benchmark/      Benchmark HumanEval Fortran
datasets/       Datasets, statistiques et scripts de construction
evaluation/     Scripts de génération et d’évaluation des programmes
inference/      Configurations utilisées pour l’inférence
results/        Résultats, générations, évaluations, analyses et figures
training/       Configurations et scripts de fine-tuning
docs/           Documentation complémentaire
