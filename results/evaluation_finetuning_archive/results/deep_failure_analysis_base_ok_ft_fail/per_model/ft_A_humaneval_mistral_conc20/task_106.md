# Failure case: ft_A_humaneval_mistral_conc20 / task 106

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ok`


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
    "ft": 6
  },
  "num_lines": {
    "base": 34,
    "ft": 52
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 44
  },
  "uses_read_stdin": {
    "base": false,
    "ft": true
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
program main
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  result = f(n)
  
  ! Output the result
  write(*,*) result
contains

  function f(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: res(:)
    integer :: i
    
    allocate(res(n))
    do i = 1, n
      if (mod(i, 2) == 0) then
        res(i) = factorial(i)
      else
        res(i) = sum_to(i)
      end if
    end do
  end function f

  function factorial(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res, i
    res = 1
    do i = 1, n
      res = res * i
    end do
  end function factorial

  function sum_to(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res, i
    res = 0
    do i = 1, n
      res = res + i
    end do
  end function sum_to

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,34 +1,52 @@
-program factorial_sum_array
+program main
+  implicit none
+  integer :: n
+  integer, allocatable :: result(:)
+  
+  ! Read input
+  read(*,*) n
+  
+  ! Call the function
+  result = f(n)
+  
+  ! Output the result
+  write(*,*) result
+contains
+
+  function f(n) result(res)
     implicit none
-    integer :: n, i, j
-    integer, allocatable :: result(:)
-    integer :: factorial, sum_val
+    integer, intent(in) :: n
+    integer, allocatable :: res(:)
+    integer :: i
+    
+    allocate(res(n))
+    do i = 1, n
+      if (mod(i, 2) == 0) then
+        res(i) = factorial(i)
+      else
+        res(i) = sum_to(i)
+      end if
+    end do
+  end function f
 
-    ! Read input
-    read *, n
+  function factorial(n) result(res)
+    implicit none
+    integer, intent(in) :: n
+    integer :: res, i
+    res = 1
+    do i = 1, n
+      res = res * i
+    end do
+  end function factorial
 
-    ! Allocate array
-    allocate(result(n))
+  function sum_to(n) result(res)
+    implicit none
+    integer, intent(in) :: n
+    integer :: res, i
+    res = 0
+    do i = 1, n
+      res = res + i
+    end do
+  end function sum_to
 
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
+end program main
```
