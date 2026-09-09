# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 138

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
  "has_contains": {
    "base": false,
    "ft": true
  },
  "num_functions": {
    "base": 0,
    "ft": 2
  },
  "num_lines": {
    "base": 14,
    "ft": 16
  },
  "num_nonempty_lines": {
    "base": 11,
    "ft": 16
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
      n = 4
      result = is_equal_to_sum_even(n)
      print *, result
    contains
      logical function is_equal_to_sum_even(n)
        if (mod(n, 2) == 0 .and. n >= 8) then
           is_equal_to_sum_even = .true.
        else
           is_equal_to_sum_even = .false.
        end if
      end function is_equal_to_sum_even
    end program is_equal_to_sum_even
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,14 +1,16 @@
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
+program is_equal_to_sum_even
+      implicit none
+      integer :: n
+      logical :: result
+      n = 4
+      result = is_equal_to_sum_even(n)
+      print *, result
+    contains
+      logical function is_equal_to_sum_even(n)
+        if (mod(n, 2) == 0 .and. n >= 8) then
+           is_equal_to_sum_even = .true.
+        else
+           is_equal_to_sum_even = .false.
+        end if
+      end function is_equal_to_sum_even
+    end program is_equal_to_sum_even
```
