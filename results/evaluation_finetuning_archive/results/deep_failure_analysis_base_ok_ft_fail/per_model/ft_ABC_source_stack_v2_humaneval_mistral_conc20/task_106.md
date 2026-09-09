# Failure case: ft_ABC_source_stack_v2_humaneval_mistral_conc20 / task 106

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
    "ft": 4
  },
  "num_lines": {
    "base": 34,
    "ft": 45
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 37
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
program f_demo
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  integer :: i

  ! Read input n
  read(*,*) n

  ! Allocate result array
  allocate(result(n))

  ! Compute result
  do i = 1, n
    if (mod(i, 2) == 0) then
      result(i) = factorial(i)
    else
      result(i) = sum_to(i)
    end if
  end do

  ! Output result
  print *, result

contains

  integer function factorial(k)
    integer, intent(in) :: k
    integer :: i
    factorial = 1
    do i = 1, k
      factorial = factorial * i
    end do
  end function factorial

  integer function sum_to(k)
    integer, intent(in) :: k
    integer :: i
    sum_to = 0
    do i = 1, k
      sum_to = sum_to + i
    end do
  end function sum_to

end program f_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,34 +1,45 @@
-program factorial_sum_array
-    implicit none
-    integer :: n, i, j
-    integer, allocatable :: result(:)
-    integer :: factorial, sum_val
+program f_demo
+  implicit none
+  integer :: n
+  integer, allocatable :: result(:)
+  integer :: i
 
-    ! Read input
-    read *, n
+  ! Read input n
+  read(*,*) n
 
-    ! Allocate array
-    allocate(result(n))
+  ! Allocate result array
+  allocate(result(n))
 
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
+  ! Compute result
+  do i = 1, n
+    if (mod(i, 2) == 0) then
+      result(i) = factorial(i)
+    else
+      result(i) = sum_to(i)
+    end if
+  end do
+
+  ! Output result
+  print *, result
+
+contains
+
+  integer function factorial(k)
+    integer, intent(in) :: k
+    integer :: i
+    factorial = 1
+    do i = 1, k
+      factorial = factorial * i
     end do
+  end function factorial
 
-    ! Output result
-    do i = 1, n
-        write (*, '(I0)') result(i)
+  integer function sum_to(k)
+    integer, intent(in) :: k
+    integer :: i
+    sum_to = 0
+    do i = 1, k
+      sum_to = sum_to + i
     end do
+  end function sum_to
 
-end program factorial_sum_array
+end program f_demo
```
