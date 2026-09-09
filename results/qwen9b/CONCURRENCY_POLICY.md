# Traitement des répétitions liées à la concurrence

Lorsqu'un même fine-tuning possède plusieurs générations avec des valeurs
de concurrence différentes (`conc3`, `conc15`, `conc20`) :

- toutes les générations sont conservées pour la traçabilité ;
- la concurrence n'est pas considérée comme un axe scientifique principal ;
- pour le tableau maître provisoire des résultats, la génération obtenant
  le meilleur score HumanEval est retenue ;
- en cas d'égalité du score, la génération évaluée la plus récemment est
  retenue uniquement pour rendre la sélection déterministe.

La manière de présenter la concurrence dans le rapport sera décidée plus tard.
