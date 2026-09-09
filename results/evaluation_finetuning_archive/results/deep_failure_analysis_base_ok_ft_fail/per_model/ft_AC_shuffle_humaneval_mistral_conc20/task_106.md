# Failure case: ft_AC_shuffle_humaneval_mistral_conc20 / task 106

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


## Prompt

```text
Write a Fortran90 program that, given a positive integer n, returns an array of size n where the value of the element at index i (starting from 1) is the factorial of i if i is even, and the sum of numbers from 1 to i if i is odd.
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
  "num_lines": {
    "base": 34,
    "ft": 46
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 39
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
  },
  "uses_assumed_size": {
    "base": false,
    "ft": true
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
program factorial_sum_array
    implicit none
    integer :: n, i, j
    integer, allocatable :: result(:)
    integer :: factorial, sum_val

    ! Read input
    read *, n

    ! Allocate array
    allocate(result(n))

    ! Compute values
    do i = 1, n
        if (mod(i, 2) == 0) then
            ! Even index: factorial of i
            factorial = 1
            do j = 1, i
                factorial = factorial * j
            end do
            result(i) = factorial
        else
            ! Odd index: sum from 1 to i
            sum_val = i * (i + 1) / 2
            result(i) = sum_val
        end if
    end do

    ! Output result
    do i = 1, n
        write (*, '(I0)') result(i)
    end do

end program factorial_sum_array
```


## FT generated code

```fortran
program factorial_sum_demo
    implicit none
    integer :: n
    integer, allocatable :: result(:)
    
    ! Read input
    read(*,*) n
    
    ! Allocate and compute result
    allocate(result(n))
    call compute_factorial_sum(n, result)
    
    ! Print output
    print *, result
    
contains

    subroutine compute_factorial_sum(n, result)
        implicit none
        integer, intent(in) :: n
        integer, intent(out) :: result(*)
        integer :: i
        integer :: factorial, sum_val
        
        do i = 1, n
            if (mod(i, 2) == 0) then
                ! Even index: compute factorial
                factorial = 1
                do while (i > 1)
                    factorial = factorial * i
                    i = i - 1
                end do
                result(i) = factorial
            else
                ! Odd index: compute sum from 1 to i
                sum_val = 0
                do while (i > 0)
                    sum_val = sum_val + i
                    i = i - 1
                end do
                result(i) = sum_val
            end if
        end do
    end subroutine compute_factorial_sum

end program factorial_sum_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,34 +1,46 @@
-program factorial_sum_array
+program factorial_sum_demo
     implicit none
-    integer :: n, i, j
+    integer :: n
     integer, allocatable :: result(:)
-    integer :: factorial, sum_val
+    
+    ! Read input
+    read(*,*) n
+    
+    ! Allocate and compute result
+    allocate(result(n))
+    call compute_factorial_sum(n, result)
+    
+    ! Print output
+    print *, result
+    
+contains
 
-    ! Read input
-    read *, n
+    subroutine compute_factorial_sum(n, result)
+        implicit none
+        integer, intent(in) :: n
+        integer, intent(out) :: result(*)
+        integer :: i
+        integer :: factorial, sum_val
+        
+        do i = 1, n
+            if (mod(i, 2) == 0) then
+                ! Even index: compute factorial
+                factorial = 1
+                do while (i > 1)
+                    factorial = factorial * i
+                    i = i - 1
+                end do
+                result(i) = factorial
+            else
+                ! Odd index: compute sum from 1 to i
+                sum_val = 0
+                do while (i > 0)
+                    sum_val = sum_val + i
+                    i = i - 1
+                end do
+                result(i) = sum_val
+            end if
+        end do
+    end subroutine compute_factorial_sum
 
-    ! Allocate array
-    allocate(result(n))
-
-    ! Compute values
-    do i = 1, n
-        if (mod(i, 2) == 0) then
-            ! Even index: factorial of i
-            factorial = 1
-            do j = 1, i
-                factorial = factorial * j
-            end do
-            result(i) = factorial
-        else
-            ! Odd index: sum from 1 to i
-            sum_val = i * (i + 1) / 2
-            result(i) = sum_val
-        end if
-    end do
-
-    ! Output result
-    do i = 1, n
-        write (*, '(I0)') result(i)
-    end do
-
-end program factorial_sum_array
+end program factorial_sum_demo
```
