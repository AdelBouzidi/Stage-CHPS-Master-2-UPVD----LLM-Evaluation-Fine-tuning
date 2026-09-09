# Failure case: ft_A_humaneval_mistral_conc3 / task 106

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ineq`


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
  "num_functions": {
    "base": 0,
    "ft": 2
  },
  "num_lines": {
    "base": 34,
    "ft": 48
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 40
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
    integer, parameter :: dp = kind(1.0d0)
    integer :: n
    integer, allocatable :: result(:)
    integer :: i

    ! Read input from stdin
    read(*,*) n

    ! Call the function
    result = factorial_sum(n)

    ! Print the result
    print *, result

contains

    function factorial_sum(n) result(res)
        implicit none
        integer, intent(in) :: n
        integer, allocatable :: res(:)
        integer :: i
        integer :: sum_val
        integer :: fact_val

        allocate(res(n))

        do i = 1, n
            if (mod(i, 2) == 0) then
                fact_val = 1
                do
                    if (i <= fact_val) exit
                    fact_val = fact_val * i
                end do
                res(i) = fact_val
            else
                sum_val = 0
                do
                    if (i <= sum_val) exit
                    sum_val = sum_val + i
                end do
                res(i) = sum_val
            end if
        end do
    end function factorial_sum

end program factorial_sum_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,34 +1,48 @@
-program factorial_sum_array
+program factorial_sum_demo
     implicit none
-    integer :: n, i, j
+    integer, parameter :: dp = kind(1.0d0)
+    integer :: n
     integer, allocatable :: result(:)
-    integer :: factorial, sum_val
+    integer :: i
 
-    ! Read input
-    read *, n
+    ! Read input from stdin
+    read(*,*) n
 
-    ! Allocate array
-    allocate(result(n))
+    ! Call the function
+    result = factorial_sum(n)
 
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
+    ! Print the result
+    print *, result
 
-    ! Output result
-    do i = 1, n
-        write (*, '(I0)') result(i)
-    end do
+contains
 
-end program factorial_sum_array
+    function factorial_sum(n) result(res)
+        implicit none
+        integer, intent(in) :: n
+        integer, allocatable :: res(:)
+        integer :: i
+        integer :: sum_val
+        integer :: fact_val
+
+        allocate(res(n))
+
+        do i = 1, n
+            if (mod(i, 2) == 0) then
+                fact_val = 1
+                do
+                    if (i <= fact_val) exit
+                    fact_val = fact_val * i
+                end do
+                res(i) = fact_val
+            else
+                sum_val = 0
+                do
+                    if (i <= sum_val) exit
+                    sum_val = sum_val + i
+                end do
+                res(i) = sum_val
+            end if
+        end do
+    end function factorial_sum
+
+end program factorial_sum_demo
```
