# Failure case: ft_ABC_source_stack_v2_humaneval_mistral_conc20 / task 123

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_output_labels`

- Labels: `static_modifies_intent_in_possible, static_output_labels, status_compile_err`


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
  "has_labels_in_output": {
    "base": false,
    "ft": true
  },
  "modifies_intent_in_possible": {
    "base": false,
    "ft": true
  },
  "num_nonempty_lines": {
    "base": 53,
    "ft": 51
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
  },
  "uses_print_star": {
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
program get_odd_collatz_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: n
  integer, allocatable :: result(:)
  integer :: i, size

  ! Hardcoded input value (example: 5)
  n = 5

  ! Call the function
  call get_odd_collatz(n, result, size)

  ! Print the result
  print *, 'Result:', (result(i), i=1,size)

contains

  subroutine get_odd_collatz(n, result, size)
    implicit none
    integer, intent(in) :: n
    integer, intent(out) :: result(:)
    integer, intent(out) :: size
    integer :: i, temp, count

    temp = n
    count = 0
    do while (temp /= 1)
      if (mod(temp, 2) /= 0) then
        count = count + 1
      end if
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    if (mod(n, 2) /= 0) count = count + 1

    allocate(result(count))
    result = 0
    i = 0
    do while (temp /= 1)
      i = i + 1
      if (mod(temp, 2) /= 0) then
        result(i) = temp
      end if
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    i = i + 1
    result(i) = temp

    size = count
  end subroutine get_odd_collatz

end program get_odd_collatz_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,60 +1,60 @@
-program collatz_odds
+program get_odd_collatz_demo
+  implicit none
+  integer, parameter :: dp = kind(1.0d0)
+  integer :: n
+  integer, allocatable :: result(:)
+  integer :: i, size
+
+  ! Hardcoded input value (example: 5)
+  n = 5
+
+  ! Call the function
+  call get_odd_collatz(n, result, size)
+
+  ! Print the result
+  print *, 'Result:', (result(i), i=1,size)
+
+contains
+
+  subroutine get_odd_collatz(n, result, size)
     implicit none
-    integer :: n
-    integer, allocatable :: odd_collatz(:)
-    integer :: i, j, temp, count
+    integer, intent(in) :: n
+    integer, intent(out) :: result(:)
+    integer, intent(out) :: size
+    integer :: i, temp, count
 
-    ! Read input
-    read *, n
+    temp = n
+    count = 0
+    do while (temp /= 1)
+      if (mod(temp, 2) /= 0) then
+        count = count + 1
+      end if
+      if (mod(temp, 2) == 0) then
+        temp = temp / 2
+      else
+        temp = 3 * temp + 1
+      end if
+    end do
+    if (mod(n, 2) /= 0) count = count + 1
 
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
+    allocate(result(count))
+    result = 0
+    i = 0
+    do while (temp /= 1)
+      i = i + 1
+      if (mod(temp, 2) /= 0) then
+        result(i) = temp
+      end if
+      if (mod(temp, 2) == 0) then
+        temp = temp / 2
+      else
+        temp = 3 * temp + 1
+      end if
     end do
+    i = i + 1
+    result(i) = temp
 
-    ! Allocate array for odd numbers
-    allocate(odd_collatz(count))
-    count = 0
+    size = count
+  end subroutine get_odd_collatz
 
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
+end program get_odd_collatz_demo
```
