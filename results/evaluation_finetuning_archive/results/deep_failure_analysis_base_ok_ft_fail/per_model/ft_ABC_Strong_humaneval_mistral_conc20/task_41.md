# Failure case: ft_ABC_Strong_humaneval_mistral_conc20 / task 41

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
  "has_contains": {
    "base": false,
    "ft": true
  },
  "has_debug_words": {
    "base": false,
    "ft": true
  },
  "modifies_intent_in_possible": {
    "base": false,
    "ft": true
  },
  "num_functions": {
    "base": 0,
    "ft": 2
  },
  "num_lines": {
    "base": 9,
    "ft": 21
  },
  "num_nonempty_lines": {
    "base": 7,
    "ft": 15
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
program car_race_collision_demo
  implicit none
  integer :: n, result

  ! Read input
  read(*,*) n

  ! Compute result
  result = car_race_collision(n)

  ! Output result
  print(*,*) result

contains

  integer function car_race_collision(n)
    integer, intent(in) :: n
    car_race_collision = n * n
  end function car_race_collision

end program car_race_collision_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,9 +1,21 @@
-program car_race_collision
-    implicit none
-    integer :: n, collisions
-    
-    read *, n
-    collisions = n * n
-    
-    print *, collisions
-end program car_race_collision
+program car_race_collision_demo
+  implicit none
+  integer :: n, result
+
+  ! Read input
+  read(*,*) n
+
+  ! Compute result
+  result = car_race_collision(n)
+
+  ! Output result
+  print(*,*) result
+
+contains
+
+  integer function car_race_collision(n)
+    integer, intent(in) :: n
+    car_race_collision = n * n
+  end function car_race_collision
+
+end program car_race_collision_demo
```
