# Failure case: ft_ABC_source_numericalhub_humaneval_mistral_conc20 / task 2

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ok`


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
  "num_lines": {
    "base": 13,
    "ft": 25
  },
  "num_nonempty_lines": {
    "base": 10,
    "ft": 19
  },
  "uses_print_star": {
    "base": false,
    "ft": true
  },
  "uses_read_stdin": {
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
program truncate_number_demo
  implicit none
  real :: number, result

  ! Read input from stdin
  read(*,*) number

  ! Call the function
  result = truncate_number(number)

  ! Write output to stdout
  print *, result

contains

  function truncate_number(number) result(res)
    implicit none
    real, intent(in) :: number
    real :: res
    integer :: int_part
    int_part = int(number)
    res = number - int_part
  end function truncate_number

end program truncate_number_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,13 +1,25 @@
-program truncate_number
+program truncate_number_demo
+  implicit none
+  real :: number, result
+
+  ! Read input from stdin
+  read(*,*) number
+
+  ! Call the function
+  result = truncate_number(number)
+
+  ! Write output to stdout
+  print *, result
+
+contains
+
+  function truncate_number(number) result(res)
     implicit none
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
+    real, intent(in) :: number
+    real :: res
+    integer :: int_part
+    int_part = int(number)
+    res = number - int_part
+  end function truncate_number
+
+end program truncate_number_demo
```
