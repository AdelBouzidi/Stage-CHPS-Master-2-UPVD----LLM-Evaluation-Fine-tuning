# Failure case: ft_C_then_A_humaneval_mistral_conc3 / task 41

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ineq`


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
  "has_debug_words": {
    "base": false,
    "ft": true
  },
  "num_nonempty_lines": {
    "base": 7,
    "ft": 8
  },
  "uses_read_stdin": {
    "base": false,
    "ft": true
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
program car_race_collision
  implicit none
  integer :: n
  integer :: result

  read(*,*) n
  result = n * n
  print *, result
end program car_race_collision
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,9 +1,9 @@
 program car_race_collision
-    implicit none
-    integer :: n, collisions
-    
-    read *, n
-    collisions = n * n
-    
-    print *, collisions
+  implicit none
+  integer :: n
+  integer :: result
+
+  read(*,*) n
+  result = n * n
+  print *, result
 end program car_race_collision
```
