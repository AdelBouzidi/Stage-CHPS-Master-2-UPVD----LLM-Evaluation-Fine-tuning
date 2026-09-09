# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 41

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that computes the number of collisions in a car race given the number of cars in each direction on a straight road.
```


## FT stderr / error

```text

```


## FT stdout

```text

```


## Expected output

```text

```


## Static feature differences base -> FT

```json
{
  "has_program": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 9,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 7,
    "ft": 0
  },
  "uses_implicit_none": {
    "base": true,
    "ft": false
  },
  "uses_print_star": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program car_race_collision
    implicit none
    integer :: n, collisions
    
    read *, n
    collisions = n * n
    
    print *, collisions
end program car_race_collision
```


## FT generated code

```fortran

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,9 +0,0 @@
-program car_race_collision
-    implicit none
-    integer :: n, collisions
-    
-    read *, n
-    collisions = n * n
-    
-    print *, collisions
-end program car_race_collision
```
