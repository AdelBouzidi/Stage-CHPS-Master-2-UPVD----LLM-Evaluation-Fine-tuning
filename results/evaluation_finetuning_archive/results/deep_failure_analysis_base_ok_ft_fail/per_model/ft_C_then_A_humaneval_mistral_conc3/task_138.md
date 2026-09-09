# Failure case: ft_C_then_A_humaneval_mistral_conc3 / task 138

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ineq`


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
  "uses_read_stdin": {
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

    ! Read input
    read(*,*) n

    ! Check if n can be written as sum of 4 positive even numbers
    result = (n >= 8) .and. (mod(n, 2) == 0)

    ! Output result
    print *, result
end program is_equal_to_sum_even
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,14 +1,14 @@
-program sum_even_check
+program is_equal_to_sum_even
     implicit none
     integer :: n
     logical :: result
-    
-    read *, n
-    
+
+    ! Read input
+    read(*,*) n
+
     ! Check if n can be written as sum of 4 positive even numbers
-    ! Minimum sum is 2+2+2+2 = 8
-    ! Sum of 4 even numbers must be even
     result = (n >= 8) .and. (mod(n, 2) == 0)
-    
+
+    ! Output result
     print *, result
-end program sum_even_check
+end program is_equal_to_sum_even
```
