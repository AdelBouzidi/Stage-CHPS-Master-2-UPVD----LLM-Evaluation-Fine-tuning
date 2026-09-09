# Failure case: ft_ABC_Strong_humaneval_mistral_conc3 / task 41

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_compile_err`


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
  "num_lines": {
    "base": 9,
    "ft": 15
  },
  "num_nonempty_lines": {
    "base": 7,
    "ft": 11
  },
  "uses_print_star": {
    "base": true,
    "ft": false
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
  integer :: collisions

  ! Read input
  read(*,*) n

  ! Calculate collisions
  collisions = n * n

  ! Output result
  print(*,*) collisions

end program car_race_collision
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,9 +1,15 @@
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
+  integer :: collisions
+
+  ! Read input
+  read(*,*) n
+
+  ! Calculate collisions
+  collisions = n * n
+
+  ! Output result
+  print(*,*) collisions
+
 end program car_race_collision
```
