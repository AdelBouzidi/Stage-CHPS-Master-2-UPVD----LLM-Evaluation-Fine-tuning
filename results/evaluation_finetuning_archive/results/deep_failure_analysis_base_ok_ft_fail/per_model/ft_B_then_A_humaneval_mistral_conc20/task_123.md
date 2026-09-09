# Failure case: ft_B_then_A_humaneval_mistral_conc20 / task 123

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `status_ineq`

- Labels: `static_modifies_intent_in_possible, status_ineq`


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
    "base": 60,
    "ft": 73
  },
  "num_nonempty_lines": {
    "base": 53,
    "ft": 64
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
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

      read *, n
      result = get_odd_collatz(n)
      write (*, '(100i0)') result

    contains

      function get_odd_collatz(n) result(arr)
        implicit none
        integer, intent(in) :: n
        integer, allocatable :: arr(:)
        integer :: i, temp, size
        integer, allocatable :: temp_arr(:)

        size = 0
        i = n
        do while (i /= 1)
          if (mod(i, 2) /= 0) then
            size = size + 1
          end if
          if (mod(i, 2) == 0) then
            i = i / 2
          else
            i = 3 * i + 1
          end if
        end do
        if (mod(n, 2) /= 0) then
          size = size + 1
        end if

        allocate(arr(size))
        i = 1
        temp = n
        do while (temp /= 1)
          if (mod(temp, 2) /= 0) then
            arr(i) = temp
            i = i + 1
          end if
          if (mod(temp, 2) == 0) then
            temp = temp / 2
          else
            temp = 3 * temp + 1
          end if
        end do
        if (mod(temp, 2) /= 0) then
          arr(i) = temp
          i = i + 1
        end if

        call sort_array(arr)

      end function get_odd_collatz

      subroutine sort_array(arr)
        implicit none
        integer, intent(inout) :: arr(:)
        integer :: i, j, temp
        do i = 1, size(arr) - 1
          do j = i + 1, size(arr)
            if (arr(j) < arr(i)) then
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
@@ -1,60 +1,73 @@
-program collatz_odds
-    implicit none
-    integer :: n
-    integer, allocatable :: odd_collatz(:)
-    integer :: i, j, temp, count
+program collatz_odd
+      implicit none
+      integer :: n
+      integer, allocatable :: result(:)
 
-    ! Read input
-    read *, n
+      read *, n
+      result = get_odd_collatz(n)
+      write (*, '(100i0)') result
 
-    ! Collect odd numbers from Collatz sequence
-    count = 0
-    temp = n
-    do while (temp > 0)
-        if (mod(temp, 2) == 1) then
-            count = count + 1
+    contains
+
+      function get_odd_collatz(n) result(arr)
+        implicit none
+        integer, intent(in) :: n
+        integer, allocatable :: arr(:)
+        integer :: i, temp, size
+        integer, allocatable :: temp_arr(:)
+
+        size = 0
+        i = n
+        do while (i /= 1)
+          if (mod(i, 2) /= 0) then
+            size = size + 1
+          end if
+          if (mod(i, 2) == 0) then
+            i = i / 2
+          else
+            i = 3 * i + 1
+          end if
+        end do
+        if (mod(n, 2) /= 0) then
+          size = size + 1
         end if
-        if (temp == 1) exit
-        if (mod(temp, 2) == 0) then
+
+        allocate(arr(size))
+        i = 1
+        temp = n
+        do while (temp /= 1)
+          if (mod(temp, 2) /= 0) then
+            arr(i) = temp
+            i = i + 1
+          end if
+          if (mod(temp, 2) == 0) then
             temp = temp / 2
-        else
+          else
             temp = 3 * temp + 1
+          end if
+        end do
+        if (mod(temp, 2) /= 0) then
+          arr(i) = temp
+          i = i + 1
         end if
-    end do
 
-    ! Allocate array for odd numbers
-    allocate(odd_collatz(count))
-    count = 0
+        call sort_array(arr)
 
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
+      end function get_odd_collatz
 
-    ! Sort the odd numbers using bubble sort
-    do i = 1, count - 1
-        do j = i + 1, count
-            if (odd_collatz(i) > odd_collatz(j)) then
-                odd_collatz(i) = odd_collatz(i) + odd_collatz(j)
-                odd_collatz(j) = odd_collatz(i) - odd_collatz(j)
-                odd_collatz(i) = odd_collatz(i) - odd_collatz(j)
+      subroutine sort_array(arr)
+        implicit none
+        integer, intent(inout) :: arr(:)
+        integer :: i, j, temp
+        do i = 1, size(arr) - 1
+          do j = i + 1, size(arr)
+            if (arr(j) < arr(i)) then
+              temp = arr(i)
+              arr(i) = arr(j)
+              arr(j) = temp
             end if
+          end do
         end do
-    end do
+      end subroutine sort_array
 
-    ! Output the sorted odd numbers
-    do i = 1, count
-        write (*, '(I0)') odd_collatz(i)
-    end do
-
-end program collatz_odds
+    end program collatz_odd
```
