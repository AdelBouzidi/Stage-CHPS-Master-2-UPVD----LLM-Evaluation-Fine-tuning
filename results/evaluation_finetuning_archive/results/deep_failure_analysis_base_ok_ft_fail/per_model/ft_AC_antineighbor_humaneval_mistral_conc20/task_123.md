# Failure case: ft_AC_antineighbor_humaneval_mistral_conc20 / task 123

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_stdin_read, status_ineq`


## Prompt

```text
Write a Fortran90 program that returns a sorted array containing the odd numbers present in the Collatz sequence of a given positive integer.
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
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 60,
    "ft": 34
  },
  "num_nonempty_lines": {
    "base": 53,
    "ft": 28
  },
  "uses_read_stdin": {
    "base": false,
    "ft": true
  }
}
```


## Base generated code

```fortran
program collatz_odds
    implicit none
    integer :: n
    integer, allocatable :: odd_collatz(:)
    integer :: i, j, temp, count

    ! Read input
    read *, n

    ! Collect odd numbers from Collatz sequence
    count = 0
    temp = n
    do while (temp > 0)
        if (mod(temp, 2) == 1) then
            count = count + 1
        end if
        if (temp == 1) exit
        if (mod(temp, 2) == 0) then
            temp = temp / 2
        else
            temp = 3 * temp + 1
        end if
    end do

    ! Allocate array for odd numbers
    allocate(odd_collatz(count))
    count = 0

    ! Collect odd numbers again
    temp = n
    do while (temp > 0)
        if (mod(temp, 2) == 1) then
            count = count + 1
            odd_collatz(count) = temp
        end if
        if (temp == 1) exit
        if (mod(temp, 2) == 0) then
            temp = temp / 2
        else
            temp = 3 * temp + 1
        end if
    end do

    ! Sort the odd numbers using bubble sort
    do i = 1, count - 1
        do j = i + 1, count
            if (odd_collatz(i) > odd_collatz(j)) then
                odd_collatz(i) = odd_collatz(i) + odd_collatz(j)
                odd_collatz(j) = odd_collatz(i) - odd_collatz(j)
                odd_collatz(i) = odd_collatz(i) - odd_collatz(j)
            end if
        end do
    end do

    ! Output the sorted odd numbers
    do i = 1, count
        write (*, '(I0)') odd_collatz(i)
    end do

end program collatz_odds
```


## FT generated code

```fortran
program collatz_odd
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  integer :: i

  ! Read input
  read(*,*) n

  ! Initialize result array
  allocate(result(n))
  i = 0

  ! Generate Collatz sequence and collect odd numbers
  do while (n /= 1)
    if (mod(n, 2) /= 0) then
      i = i + 1
      result(i) = n
    end if
    if (mod(n, 2) == 0) then
      n = n / 2
    else
      n = 3 * n + 1
    end if
  end do

  ! Add the final 1 if it's odd (it always is)
  i = i + 1
  result(i) = 1

  ! Output result
  write(*,*) result

end program collatz_odd
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,60 +1,34 @@
-program collatz_odds
-    implicit none
-    integer :: n
-    integer, allocatable :: odd_collatz(:)
-    integer :: i, j, temp, count
+program collatz_odd
+  implicit none
+  integer :: n
+  integer, allocatable :: result(:)
+  integer :: i
 
-    ! Read input
-    read *, n
+  ! Read input
+  read(*,*) n
 
-    ! Collect odd numbers from Collatz sequence
-    count = 0
-    temp = n
-    do while (temp > 0)
-        if (mod(temp, 2) == 1) then
-            count = count + 1
-        end if
-        if (temp == 1) exit
-        if (mod(temp, 2) == 0) then
-            temp = temp / 2
-        else
-            temp = 3 * temp + 1
-        end if
-    end do
+  ! Initialize result array
+  allocate(result(n))
+  i = 0
 
-    ! Allocate array for odd numbers
-    allocate(odd_collatz(count))
-    count = 0
+  ! Generate Collatz sequence and collect odd numbers
+  do while (n /= 1)
+    if (mod(n, 2) /= 0) then
+      i = i + 1
+      result(i) = n
+    end if
+    if (mod(n, 2) == 0) then
+      n = n / 2
+    else
+      n = 3 * n + 1
+    end if
+  end do
 
-    ! Collect odd numbers again
-    temp = n
-    do while (temp > 0)
-        if (mod(temp, 2) == 1) then
-            count = count + 1
-            odd_collatz(count) = temp
-        end if
-        if (temp == 1) exit
-        if (mod(temp, 2) == 0) then
-            temp = temp / 2
-        else
-            temp = 3 * temp + 1
-        end if
-    end do
+  ! Add the final 1 if it's odd (it always is)
+  i = i + 1
+  result(i) = 1
 
-    ! Sort the odd numbers using bubble sort
-    do i = 1, count - 1
-        do j = i + 1, count
-            if (odd_collatz(i) > odd_collatz(j)) then
-                odd_collatz(i) = odd_collatz(i) + odd_collatz(j)
-                odd_collatz(j) = odd_collatz(i) - odd_collatz(j)
-                odd_collatz(i) = odd_collatz(i) - odd_collatz(j)
-            end if
-        end do
-    end do
+  ! Output result
+  write(*,*) result
 
-    ! Output the sorted odd numbers
-    do i = 1, count
-        write (*, '(I0)') odd_collatz(i)
-    end do
-
-end program collatz_odds
+end program collatz_odd
```
