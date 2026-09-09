# Failure case: ft_ABC_source_burkardt_humaneval_mistral_conc20 / task 123

- Base status: `ok`

- FT status: `exception`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_exception`


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
  "has_contains": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 60,
    "ft": 58
  },
  "num_nonempty_lines": {
    "base": 53,
    "ft": 50
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
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
  integer, allocatable :: odd_collatz(:)
  integer :: i, temp, count

  read(*,*) n

  count = 0
  temp = n
  do while (temp > 0)
    if (mod(temp, 2) == 1) then
      count = count + 1
    end if
    if (mod(temp, 2) == 0) then
      temp = temp / 2
    else
      temp = 3 * temp + 1
    end if
  end do

  allocate(odd_collatz(count))
  i = 0
  temp = n
  do while (temp > 0)
    if (mod(temp, 2) == 1) then
      i = i + 1
      odd_collatz(i) = temp
    end if
    if (mod(temp, 2) == 0) then
      temp = temp / 2
    else
      temp = 3 * temp + 1
    end if
  end do

  call sort_array(odd_collatz)

  write(*,*) odd_collatz

contains

  subroutine sort_array(arr)
    implicit none
    integer, intent(inout), allocatable :: arr(:)
    integer :: i, j, temp
    do i = 1, size(arr) - 1
      do j = i + 1, size(arr)
        if (arr(i) > arr(j)) then
          temp = arr(i)
          arr(i) = arr(j)
          arr(j) = temp
        end if
      end do
    end do
  end subroutine sort_array

end program collatz_odd
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,60 +1,58 @@
-program collatz_odds
+program collatz_odd
+  implicit none
+  integer :: n
+  integer, allocatable :: odd_collatz(:)
+  integer :: i, temp, count
+
+  read(*,*) n
+
+  count = 0
+  temp = n
+  do while (temp > 0)
+    if (mod(temp, 2) == 1) then
+      count = count + 1
+    end if
+    if (mod(temp, 2) == 0) then
+      temp = temp / 2
+    else
+      temp = 3 * temp + 1
+    end if
+  end do
+
+  allocate(odd_collatz(count))
+  i = 0
+  temp = n
+  do while (temp > 0)
+    if (mod(temp, 2) == 1) then
+      i = i + 1
+      odd_collatz(i) = temp
+    end if
+    if (mod(temp, 2) == 0) then
+      temp = temp / 2
+    else
+      temp = 3 * temp + 1
+    end if
+  end do
+
+  call sort_array(odd_collatz)
+
+  write(*,*) odd_collatz
+
+contains
+
+  subroutine sort_array(arr)
     implicit none
-    integer :: n
-    integer, allocatable :: odd_collatz(:)
-    integer :: i, j, temp, count
+    integer, intent(inout), allocatable :: arr(:)
+    integer :: i, j, temp
+    do i = 1, size(arr) - 1
+      do j = i + 1, size(arr)
+        if (arr(i) > arr(j)) then
+          temp = arr(i)
+          arr(i) = arr(j)
+          arr(j) = temp
+        end if
+      end do
+    end do
+  end subroutine sort_array
 
-    ! Read input
-    read *, n
-
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
-
-    ! Allocate array for odd numbers
-    allocate(odd_collatz(count))
-    count = 0
-
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
-
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
-
-end program collatz_odds
+end program collatz_odd
```
