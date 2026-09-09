# Failure case: ft_ABC_dedup_BC_humaneval_mistral_conc20 / task 123

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ineq`


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
    "ft": 77
  },
  "num_nonempty_lines": {
    "base": 53,
    "ft": 68
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
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
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  result = get_odd_collatz(n)
  
  ! Print output
  print *, result
contains

  function get_odd_collatz(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: res(:)
    integer :: i, temp
    integer :: count = 0
    
    ! Calculate the Collatz sequence and count odd numbers
    temp = n
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
    if (mod(n, 2) /= 0) then
      count = count + 1
    end if
    
    allocate(res(count))
    i = 0
    temp = n
    do while (temp /= 1)
      if (mod(temp, 2) /= 0) then
        i = i + 1
        res(i) = temp
      end if
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    if (mod(n, 2) /= 0) then
      i = i + 1
      res(i) = n
    end if
    
    ! Sort the result array
    call sort_array(res)
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

end program get_odd_collatz_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,60 +1,77 @@
-program collatz_odds
+program get_odd_collatz_demo
+  implicit none
+  integer :: n
+  integer, allocatable :: result(:)
+  
+  ! Read input
+  read(*,*) n
+  
+  ! Call the function
+  result = get_odd_collatz(n)
+  
+  ! Print output
+  print *, result
+contains
+
+  function get_odd_collatz(n) result(res)
     implicit none
-    integer :: n
-    integer, allocatable :: odd_collatz(:)
-    integer :: i, j, temp, count
+    integer, intent(in) :: n
+    integer, allocatable :: res(:)
+    integer :: i, temp
+    integer :: count = 0
+    
+    ! Calculate the Collatz sequence and count odd numbers
+    temp = n
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
+    if (mod(n, 2) /= 0) then
+      count = count + 1
+    end if
+    
+    allocate(res(count))
+    i = 0
+    temp = n
+    do while (temp /= 1)
+      if (mod(temp, 2) /= 0) then
+        i = i + 1
+        res(i) = temp
+      end if
+      if (mod(temp, 2) == 0) then
+        temp = temp / 2
+      else
+        temp = 3 * temp + 1
+      end if
+    end do
+    if (mod(n, 2) /= 0) then
+      i = i + 1
+      res(i) = n
+    end if
+    
+    ! Sort the result array
+    call sort_array(res)
+  end function get_odd_collatz
 
-    ! Read input
-    read *, n
+  subroutine sort_array(arr)
+    implicit none
+    integer, intent(inout) :: arr(:)
+    integer :: i, j, temp
+    do i = 1, size(arr) - 1
+      do j = i + 1, size(arr)
+        if (arr(j) < arr(i)) then
+          temp = arr(i)
+          arr(i) = arr(j)
+          arr(j) = temp
+        end if
+      end do
+    end do
+  end subroutine sort_array
 
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
+end program get_odd_collatz_demo
```
