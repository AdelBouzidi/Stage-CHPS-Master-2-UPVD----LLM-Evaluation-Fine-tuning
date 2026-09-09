# Failure case: ft_B_humaneval_mistral_conc20 / task 138

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `status_ok`


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
  "num_lines": {
    "base": 14,
    "ft": 15
  },
  "num_nonempty_lines": {
    "base": 11,
    "ft": 12
  },
  "uses_hardcoded_scalars": {
    "base": false,
    "ft": true
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
program is_equal_to_sum_even
    implicit none
    integer :: n
    logical :: result
    
    read *, n
    
    if (n >= 8 .and. mod(n, 2) == 0) then
        result = .true.
    else
        result = .false.
    end if
    
    print *, result
end program is_equal_to_sum_even
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,14 +1,15 @@
-program sum_even_check
+program is_equal_to_sum_even
     implicit none
     integer :: n
     logical :: result
     
     read *, n
     
-    ! Check if n can be written as sum of 4 positive even numbers
-    ! Minimum sum is 2+2+2+2 = 8
-    ! Sum of 4 even numbers must be even
-    result = (n >= 8) .and. (mod(n, 2) == 0)
+    if (n >= 8 .and. mod(n, 2) == 0) then
+        result = .true.
+    else
+        result = .false.
+    end if
     
     print *, result
-end program sum_even_check
+end program is_equal_to_sum_even
```
