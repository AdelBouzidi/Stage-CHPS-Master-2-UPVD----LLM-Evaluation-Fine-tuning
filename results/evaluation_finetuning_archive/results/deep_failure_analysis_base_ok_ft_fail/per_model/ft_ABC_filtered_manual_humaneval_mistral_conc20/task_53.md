# Failure case: ft_ABC_filtered_manual_humaneval_mistral_conc20 / task 53

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that adds two numbers.
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
    "base": true,
    "ft": false
  },
  "has_program": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 9,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 8,
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
program add_numbers
    implicit none
    integer :: x, y, result
    
    read *, x
    read *, y
    result = x + y
    print *, result
end program add_numbers
```


## FT generated code

```fortran

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,9 +0,0 @@
-program add_numbers
-    implicit none
-    integer :: x, y, result
-    
-    read *, x
-    read *, y
-    result = x + y
-    print *, result
-end program add_numbers
```
