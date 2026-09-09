# Failure case: ft_ABC_source_numerical_methods_humaneval_mistral_conc20 / task 2

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
  "num_lines": {
    "base": 13,
    "ft": 14
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
program decimal_part
    implicit none
    real :: number, decimal_part
    
    ! Read input from stdin
    read *, number
    
    ! Calculate decimal part by subtracting integer part
    decimal_part = number - int(number)
    
    ! Write output to stdout
    write (*, *) decimal_part
    
end program decimal_part
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,4 +1,4 @@
-program truncate_number
+program decimal_part
     implicit none
     real :: number, decimal_part
     
@@ -10,4 +10,5 @@
     
     ! Write output to stdout
     write (*, *) decimal_part
-end program truncate_number
+    
+end program decimal_part
```
