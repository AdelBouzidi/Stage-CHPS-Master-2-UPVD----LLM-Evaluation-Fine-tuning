# Failure case: ft_B_humaneval_mistral_conc20 / task 123

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, status_ineq`


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
  "num_lines": {
    "base": 60,
    "ft": 50
  },
  "num_nonempty_lines": {
    "base": 53,
    "ft": 44
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
program collatz_odds
  implicit none
  integer :: n, current
  integer, allocatable :: odd_numbers(:)
  integer :: count, i

  ! Read input
  read *, n

  ! Generate Collatz sequence and collect odd numbers
  current = n
  count = 0
  do
    if (mod(current, 2) == 1) then
      count = count + 1
    end if
    if (current == 1) exit
    if (mod(current, 2) == 0) then
      current = current / 2
    else
      current = 3 * current + 1
    end if
  end do

  ! Allocate array for odd numbers
  allocate(odd_numbers(count))

  ! Collect odd numbers
  current = n
  i = 1
  do
    if (mod(current, 2) == 1) then
      odd_numbers(i) = current
      i = i + 1
    end if
    if (current == 1) exit
    if (mod(current, 2) == 0) then
      current = current / 2
    else
      current = 3 * current + 1
    end if
  end do

  ! Output odd numbers separated by spaces
  do i = 1, count
    if (i > 1) write (*, *) ' '
    write (*, *) odd_numbers(i)
  end do

end program collatz_odds
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,60 +1,50 @@
 program collatz_odds
-    implicit none
-    integer :: n
-    integer, allocatable :: odd_collatz(:)
-    integer :: i, j, temp, count
+  implicit none
+  integer :: n, current
+  integer, allocatable :: odd_numbers(:)
+  integer :: count, i
 
-    ! Read input
-    read *, n
+  ! Read input
+  read *, n
 
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
+  ! Generate Collatz sequence and collect odd numbers
+  current = n
+  count = 0
+  do
+    if (mod(current, 2) == 1) then
+      count = count + 1
+    end if
+    if (current == 1) exit
+    if (mod(current, 2) == 0) then
+      current = current / 2
+    else
+      current = 3 * current + 1
+    end if
+  end do
 
-    ! Allocate array for odd numbers
-    allocate(odd_collatz(count))
-    count = 0
+  ! Allocate array for odd numbers
+  allocate(odd_numbers(count))
 
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
+  ! Collect odd numbers
+  current = n
+  i = 1
+  do
+    if (mod(current, 2) == 1) then
+      odd_numbers(i) = current
+      i = i + 1
+    end if
+    if (current == 1) exit
+    if (mod(current, 2) == 0) then
+      current = current / 2
+    else
+      current = 3 * current + 1
+    end if
+  end do
 
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
-
-    ! Output the sorted odd numbers
-    do i = 1, count
-        write (*, '(I0)') odd_collatz(i)
-    end do
+  ! Output odd numbers separated by spaces
+  do i = 1, count
+    if (i > 1) write (*, *) ' '
+    write (*, *) odd_numbers(i)
+  end do
 
 end program collatz_odds
```
