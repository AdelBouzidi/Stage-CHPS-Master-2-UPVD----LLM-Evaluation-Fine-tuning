# Failure case: ft_B_humaneval_mistral_conc20 / task 106

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `static_modifies_intent_in_possible, status_ok`


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
    "ft": 40
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 31
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
program factorial_sum
  implicit none
  integer :: n, i
  integer, allocatable :: result(:)
  
  read *, n
  
  allocate(result(n))
  
  do i = 1, n
    if (mod(i, 2) == 0) then
      result(i) = factorial(i)
    else
      result(i) = sum_to(i)
    end if
  end do
  
  write (*, *) (result(i), i = 1, n)
  
  deallocate(result)
  
contains
  
  recursive function factorial(k) result(fact)
    integer, intent(in) :: k
    integer :: fact
    if (k <= 1) then
      fact = 1
    else
      fact = k * factorial(k - 1)
    end if
  end function factorial
  
  function sum_to(k) result(s)
    integer, intent(in) :: k
    integer :: s
    s = k * (k + 1) / 2
  end function sum_to
  
end program factorial_sum
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,34 +1,40 @@
-program factorial_sum_array
-    implicit none
-    integer :: n, i, j
-    integer, allocatable :: result(:)
-    integer :: factorial, sum_val
-
-    ! Read input
-    read *, n
-
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
+program factorial_sum
+  implicit none
+  integer :: n, i
+  integer, allocatable :: result(:)
+  
+  read *, n
+  
+  allocate(result(n))
+  
+  do i = 1, n
+    if (mod(i, 2) == 0) then
+      result(i) = factorial(i)
+    else
+      result(i) = sum_to(i)
+    end if
+  end do
+  
+  write (*, *) (result(i), i = 1, n)
+  
+  deallocate(result)
+  
+contains
+  
+  recursive function factorial(k) result(fact)
+    integer, intent(in) :: k
+    integer :: fact
+    if (k <= 1) then
+      fact = 1
+    else
+      fact = k * factorial(k - 1)
+    end if
+  end function factorial
+  
+  function sum_to(k) result(s)
+    integer, intent(in) :: k
+    integer :: s
+    s = k * (k + 1) / 2
+  end function sum_to
+  
+end program factorial_sum
```
