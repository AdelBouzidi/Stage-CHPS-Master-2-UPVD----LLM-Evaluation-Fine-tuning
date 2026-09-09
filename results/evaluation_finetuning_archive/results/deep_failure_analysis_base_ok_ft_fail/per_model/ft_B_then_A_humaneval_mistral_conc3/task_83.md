# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 83

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that returns the count of n-digit positive integers that start or end with 1.
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
    "base": 16,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 12,
    "ft": 0
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  },
  "uses_implicit_none": {
    "base": true,
    "ft": false
  },
  "uses_read_stdin": {
    "base": true,
    "ft": false
  },
  "uses_write_star": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program count_start_or_end_one
    implicit none
    integer :: n
    integer :: result

    read(*,*) n

    if (n == 1) then
        result = 1
    else
        result = 18 * 10**(n - 2)
    end if

    write(*,*) result

end program count_start_or_end_one
```


## FT generated code

```fortran

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,16 +0,0 @@
-program count_start_or_end_one
-    implicit none
-    integer :: n
-    integer :: result
-
-    read(*,*) n
-
-    if (n == 1) then
-        result = 1
-    else
-        result = 18 * 10**(n - 2)
-    end if
-
-    write(*,*) result
-
-end program count_start_or_end_one
```
