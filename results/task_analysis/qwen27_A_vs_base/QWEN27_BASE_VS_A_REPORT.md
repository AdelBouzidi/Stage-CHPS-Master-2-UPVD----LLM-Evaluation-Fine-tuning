# Qwen3.5-27B — base vs fine-tuning Type A

## Résultats globaux

- Base : 56/164 tâches correctes
- A archivé : 62/164
- A retenu pour le rapport : 63/164
- Erreurs de compilation A retenues : 53

La correction 62→63 est appliquée uniquement aux statistiques agrégées : +1 OK et -1 compile_err.

## Transitions tâche par tâche (run A archivé)

- acquise: 22
- regression: 16
- conservee: 40
- echec_persistant: 86

## Erreurs corrigées par le fine-tuning

- compile_err → OK : 18
- runtime_err → OK : 2
- ineq → OK : 2

### Familles détaillées corrigées

- compilation_non_detaillee: 18
- runtime_non_detaillee: 2
- sortie_incorrecte: 2

## Régressions introduites

- OK → compile_err: 13
- OK → runtime_err: 2
- OK → ineq: 1

### Familles détaillées introduites

- compilation_non_detaillee: 13
- runtime_non_detaillee: 2
- sortie_incorrecte: 1

## Échecs persistants

- compile_err → compile_err: 31
- runtime_err → runtime_err: 20
- compile_err → runtime_err: 16
- ineq → compile_err: 7
- compile_err → ineq: 6
- runtime_err → compile_err: 3
- ineq → ineq: 2
- ineq → runtime_err: 1

## Exemples de tâches acquises

### Tâche 4
Write a Fortran90 program that calculates the mean absolute deviation around the mean for a given array of numbers.
- Base : compile_err (compilation_non_detaillee)
- Après A : OK

### Tâche 8
Write a Fortran90 program that, given an array of integers, returns a tuple consisting of the sum and the product of all the integers.
- Base : runtime_err (runtime_non_detaillee)
- Après A : OK

### Tâche 15
Write a Fortran90 program that returns a string containing space‐delimited numbers starting from 0 up to n inclusive.
- Base : compile_err (compilation_non_detaillee)
- Après A : OK

### Tâche 18
Write a Fortran90 program that finds how many times a given substring can be found in the original string, counting overlapping occurrences.
- Base : compile_err (compilation_non_detaillee)
- Après A : OK

### Tâche 21
Write a Fortran90 program that given an array of numbers (of at least two elements), applies a linear transform to that array, such that the smallest number will become 0 and the largest will become 1.
- Base : runtime_err (runtime_non_detaillee)
- Après A : OK

### Tâche 31
Write a Fortran90 program that returns true if a given number is prime, and false otherwise.
- Base : compile_err (compilation_non_detaillee)
- Après A : OK

### Tâche 39
Write a Fortran90 program that returns the n-th number that is both a Fibonacci number and prime.
- Base : compile_err (compilation_non_detaillee)
- Après A : OK

### Tâche 46
Write a Fortran90 program that efficiently computes the n-th element of the Fib4 sequence without using recursion.
- Base : compile_err (compilation_non_detaillee)
- Après A : OK

### Tâche 59
Write a Fortran90 program that returns the largest prime factor of a given number. Assume the number is greater than 1 and is not a prime.
- Base : compile_err (compilation_non_detaillee)
- Après A : OK

### Tâche 62
Write a Fortran90 program that computes the derivative of a polynomial given as an array of coefficients. The polynomial is represented as xs[0] + xs[1]*x + xs[2]*x^2 + ... and the result should be in the same form.
- Base : compile_err (compilation_non_detaillee)
- Après A : OK

## Exemples de régressions

### Tâche 9
Write a Fortran90 program that, given an array of integers, returns an array of rolling maximum values found until each moment in the sequence.
- Base : OK
- Après A : runtime_err (runtime_non_detaillee)

### Tâche 13
Write a Fortran90 program that returns the greatest common divisor of two integers.
- Base : OK
- Après A : compile_err (compilation_non_detaillee)

### Tâche 20
Write a Fortran90 program that from a supplied array of numbers (of length at least two) select and return two that are the closest to each other and return them in order (smaller number, larger number).
- Base : OK
- Après A : compile_err (compilation_non_detaillee)

### Tâche 47
Write a Fortran90 program that returns the median of an array of numbers.
- Base : OK
- Après A : compile_err (compilation_non_detaillee)

### Tâche 68
Write a Fortran90 program that selects and returns a node from an array representing a tree branch. The node to pluck is the one with the smallest even value; if there are multiple, choose the one with the smallest index. Return the plucked node as an array [value, index]. If no even number exists or the array is empty, return an empty array.
- Base : OK
- Après A : compile_err (compilation_non_detaillee)

### Tâche 77
Write a Fortran90 program that takes an integer and returns true if it is the cube of some integer, and false otherwise.
- Base : OK
- Après A : compile_err (compilation_non_detaillee)

### Tâche 83
Write a Fortran90 program that returns the count of n-digit positive integers that start or end with 1.
- Base : OK
- Après A : compile_err (compilation_non_detaillee)

### Tâche 85
Write a Fortran90 program that sums the even elements of an array that are located at odd indices.
- Base : OK
- Après A : compile_err (compilation_non_detaillee)

### Tâche 88
Write a Fortran90 program that, given an array of non-negative integers, returns a sorted copy of the array. Sort in ascending order if the sum of the first and last elements is odd, otherwise sort in descending order.
- Base : OK
- Après A : runtime_err (runtime_non_detaillee)

### Tâche 102
Write a Fortran90 program that takes two positive integers x and y and returns the largest even integer within the range [x, y] inclusive. If there is no such even number, return -1.
- Base : OK
- Après A : compile_err (compilation_non_detaillee)
