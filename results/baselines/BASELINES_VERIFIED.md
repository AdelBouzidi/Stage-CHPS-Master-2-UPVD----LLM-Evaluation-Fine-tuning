# Baselines vérifiées — pipeline principal

## Qwen3.5-9B

Deux générations historiques existent.

### Run conc3
- concurrence vLLM : 3
- benchmark : 164 tâches
- OK : 38
- Pass@1 : 0.2317073171
- compile_err : 40
- runtime_err : 56
- ineq : 27
- exception : 3

### Run conc30
- concurrence vLLM : 30
- benchmark : 164 tâches
- OK : 36
- Pass@1 : 0.2195121951
- compile_err : 41
- runtime_err : 55
- ineq : 29
- exception : 3

### Référence retenue pour les analyses finales

Les scripts récents de comparaison, de régression et d'analyse détaillée
utilisent explicitement le run conc30 comme baseline :

- `evaluate_and_compare_all_available_vs_base.py`
- `diagnose_base_ok_ft_failures.py`
- `deep_analyze_base_ok_ft_failures.py`

Baseline Qwen3.5-9B retenue :
**36 / 164 = 21,95 %**

Le run conc3 (38/164) est conservé comme trace historique.

---

## Qwen3.5-27B

### Premier run conc30

Ce run est techniquement invalide comme baseline :

- 164 tâches
- 162 générations en échec
- seulement 2 codes non vides
- erreurs principales :
  - connexion refusée ;
  - connexion interrompue ;
  - timeout HTTP 600 s.

Ce run NE DOIT PAS être utilisé comme résultat scientifique.

### Run conc12

Génération :
- 164 tâches
- 164 réponses reçues
- aucune erreur HTTP
- 106 extractions `ok`
- 58 extractions `warning`
- 106 codes non vides
- 58 codes vides

Évaluation :
- OK : 56
- Pass@1 : 0.3414634146
- compile_err : 71
- runtime_err : 25
- ineq : 12
- exception : 0
- compilation_rate : 0.5670731707
- execution_success_rate : 0.4146341463

Baseline Qwen3.5-27B retenue actuellement :
**56 / 164 = 34,15 %**

Limite d'exécution de l'évaluation :
**10 secondes par tâche**

À vérifier :
- confirmer que les adaptateurs Qwen27 sont évalués avec la même limite
  de 10 secondes.
