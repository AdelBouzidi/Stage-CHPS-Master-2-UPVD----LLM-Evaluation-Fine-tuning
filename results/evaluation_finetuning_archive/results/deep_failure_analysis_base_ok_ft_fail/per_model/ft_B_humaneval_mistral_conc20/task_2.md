# Failure case: ft_B_humaneval_mistral_conc20 / task 2

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


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
    "ft": 8
  },
  "num_nonempty_lines": {
    "base": 10,
    "ft": 7
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
program truncate_number
  implicit none
  real :: number, result
  
  read *, number
  result = number - int(number)
  write *, result
end program truncate_number
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,13 +1,8 @@
 program truncate_number
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
+  implicit none
+  real :: number, result
+  
+  read *, number
+  result = number - int(number)
+  write *, result
 end program truncate_number
```
