# Failure case: ft_B_then_A_humaneval_mistral_conc20 / task 24

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that for a given number n, finds the largest number that divides n evenly, smaller than n.
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
    "base": 21,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 18,
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
  "uses_write_star": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program largest_divisor
    implicit none
    integer :: n, i, result
    
    ! Read input
    read *, n
    
    ! Find largest divisor smaller than n
    result = 1
    if (n > 1) then
        do i = n/2, 1, -1
            if (mod(n, i) == 0) then
                result = i
                exit
            end if
        end do
    end if
    
    ! Output result
    write (*, *) result
end program largest_divisor
```


## FT generated code

```fortran

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,21 +0,0 @@
-program largest_divisor
-    implicit none
-    integer :: n, i, result
-    
-    ! Read input
-    read *, n
-    
-    ! Find largest divisor smaller than n
-    result = 1
-    if (n > 1) then
-        do i = n/2, 1, -1
-            if (mod(n, i) == 0) then
-                result = i
-                exit
-            end if
-        end do
-    end if
-    
-    ! Output result
-    write (*, *) result
-end program largest_divisor
```
