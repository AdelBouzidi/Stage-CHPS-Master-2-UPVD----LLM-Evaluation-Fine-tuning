# Failure case: ft_ABC_filtered_manual_humaneval_mistral_conc20 / task 138

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that evaluates whether the given integer n can be written as the sum of exactly 4 positive even numbers.
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
    "base": 14,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 11,
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
program sum_even_check
    implicit none
    integer :: n
    logical :: result
    
    read *, n
    
    ! Check if n can be written as sum of 4 positive even numbers
    ! Minimum sum is 2+2+2+2 = 8
    ! Sum of 4 even numbers must be even
    result = (n >= 8) .and. (mod(n, 2) == 0)
    
    print *, result
end program sum_even_check
```


## FT generated code

```fortran

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,14 +0,0 @@
-program sum_even_check
-    implicit none
-    integer :: n
-    logical :: result
-    
-    read *, n
-    
-    ! Check if n can be written as sum of 4 positive even numbers
-    ! Minimum sum is 2+2+2+2 = 8
-    ! Sum of 4 even numbers must be even
-    result = (n >= 8) .and. (mod(n, 2) == 0)
-    
-    print *, result
-end program sum_even_check
```
