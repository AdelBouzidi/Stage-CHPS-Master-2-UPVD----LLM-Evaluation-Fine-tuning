# Failure case: ft_ABC_Strong_humaneval_mistral_conc3 / task 123

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_possible_zero_indexing`

- Labels: `static_modifies_intent_in_possible, static_possible_zero_indexing, status_compile_err`


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
    "ft": 55
  },
  "num_nonempty_lines": {
    "base": 53,
    "ft": 48
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
  },
  "uses_array_index_0_literal": {
    "base": false,
    "ft": true
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
  integer, dimension(:), allocatable :: result
  integer :: n
  
  ! Hardcoded example input
  n = 5
  
  call get_odd_collatz(n, result)
  
  print *, result
contains

  subroutine get_odd_collatz(n, result)
    integer, intent(in) :: n
    integer, intent(out), allocatable :: result(:)
    integer :: i, temp
    integer, dimension(:), allocatable :: odd_nums
    
    ! Generate Collatz sequence and collect odd numbers
    allocate(odd_nums(0))
    temp = n
    do while (temp /= 1)
      if (mod(temp, 2) /= 0) then
        allocate(odd_nums(size(odd_nums) + 1))
        odd_nums(size(odd_nums)) = temp
      end if
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    allocate(result(size(odd_nums)))
    result = odd_nums
    result = sort_array(result)
  end subroutine get_odd_collatz

  function sort_array(arr) result(sorted)
    integer, intent(in) :: arr(:)
    integer :: sorted(:)
    integer :: i, j, temp
    sorted = arr
    do i = 1, size(sorted) - 1
      do j = i + 1, size(sorted)
        if (sorted(j) < sorted(i)) then
          temp = sorted(i)
          sorted(i) = sorted(j)
          sorted(j) = temp
        end if
      end do
    end do
  end function sort_array

end program get_odd_collatz_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,60 +1,55 @@
-program collatz_odds
-    implicit none
-    integer :: n
-    integer, allocatable :: odd_collatz(:)
-    integer :: i, j, temp, count
+program get_odd_collatz_demo
+  implicit none
+  integer, dimension(:), allocatable :: result
+  integer :: n
+  
+  ! Hardcoded example input
+  n = 5
+  
+  call get_odd_collatz(n, result)
+  
+  print *, result
+contains
 
-    ! Read input
-    read *, n
+  subroutine get_odd_collatz(n, result)
+    integer, intent(in) :: n
+    integer, intent(out), allocatable :: result(:)
+    integer :: i, temp
+    integer, dimension(:), allocatable :: odd_nums
+    
+    ! Generate Collatz sequence and collect odd numbers
+    allocate(odd_nums(0))
+    temp = n
+    do while (temp /= 1)
+      if (mod(temp, 2) /= 0) then
+        allocate(odd_nums(size(odd_nums) + 1))
+        odd_nums(size(odd_nums)) = temp
+      end if
+      if (mod(temp, 2) == 0) then
+        temp = temp / 2
+      else
+        temp = 3 * temp + 1
+      end if
+    end do
+    allocate(result(size(odd_nums)))
+    result = odd_nums
+    result = sort_array(result)
+  end subroutine get_odd_collatz
 
-    ! Collect odd numbers from Collatz sequence
-    count = 0
-    temp = n
-    do while (temp > 0)
-        if (mod(temp, 2) == 1) then
-            count = count + 1
+  function sort_array(arr) result(sorted)
+    integer, intent(in) :: arr(:)
+    integer :: sorted(:)
+    integer :: i, j, temp
+    sorted = arr
+    do i = 1, size(sorted) - 1
+      do j = i + 1, size(sorted)
+        if (sorted(j) < sorted(i)) then
+          temp = sorted(i)
+          sorted(i) = sorted(j)
+          sorted(j) = temp
         end if
-        if (temp == 1) exit
-        if (mod(temp, 2) == 0) then
-            temp = temp / 2
-        else
-            temp = 3 * temp + 1
-        end if
+      end do
     end do
+  end function sort_array
 
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
+end program get_odd_collatz_demo
```
