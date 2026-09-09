# Failure case: ft_ABC_filtered_reject_humaneval_mistral_conc20 / task 2

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


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
  "num_nonempty_lines": {
    "base": 10,
    "ft": 13
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
  real :: number, result
  read *, number
  result = truncate_number(number)
  print *, result
contains
  function truncate_number(number) result
    real, intent(in) :: number
    real :: result
    result = number - int(number)
  end function truncate_number
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,13 +1,13 @@
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
+  real :: number, result
+  read *, number
+  result = truncate_number(number)
+  print *, result
+contains
+  function truncate_number(number) result
+    real, intent(in) :: number
+    real :: result
+    result = number - int(number)
+  end function truncate_number
+end program main
```
