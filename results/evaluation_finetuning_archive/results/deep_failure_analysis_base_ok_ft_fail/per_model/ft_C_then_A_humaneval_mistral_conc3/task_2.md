# Failure case: ft_C_then_A_humaneval_mistral_conc3 / task 2

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `status_ineq`

- Labels: `status_ineq`


## Prompt

```text
Write a Fortran90 program that returns the decimal part of a given positive floating point number.
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
  "num_lines": {
    "base": 13,
    "ft": 12
  },
  "num_nonempty_lines": {
    "base": 10,
    "ft": 9
  },
  "uses_hardcoded_scalars": {
    "base": false,
    "ft": true
  },
  "uses_print_star": {
    "base": false,
    "ft": true
  },
  "uses_write_star": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program truncate_number
    implicit none
    real :: number, decimal_part
    
    ! Read input from stdin
    read *, number
    
    ! Calculate decimal part by subtracting integer part
    decimal_part = number - int(number)
    
    ! Write output to stdout
    write (*, *) decimal_part
end program truncate_number
```


## FT generated code

```fortran
program main
  implicit none
  real :: number
  real :: result

  ! Hardcoded input value
  number = 3.5

  result = truncate_number(number)

  print *, result
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,13 +1,12 @@
-program truncate_number
-    implicit none
-    real :: number, decimal_part
-    
-    ! Read input from stdin
-    read *, number
-    
-    ! Calculate decimal part by subtracting integer part
-    decimal_part = number - int(number)
-    
-    ! Write output to stdout
-    write (*, *) decimal_part
-end program truncate_number
+program main
+  implicit none
+  real :: number
+  real :: result
+
+  ! Hardcoded input value
+  number = 3.5
+
+  result = truncate_number(number)
+
+  print *, result
+end program main
```
