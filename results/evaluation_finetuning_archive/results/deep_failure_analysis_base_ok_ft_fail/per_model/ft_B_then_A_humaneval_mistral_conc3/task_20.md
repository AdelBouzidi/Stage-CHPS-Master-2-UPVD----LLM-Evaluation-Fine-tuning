# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 20

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, status_ineq`


## Prompt

```text
Write a Fortran90 program that from a supplied array of numbers (of length at least two) select and return two that are the closest to each other and return them in order (smaller number, larger number).
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
    "base": 37,
    "ft": 30
  },
  "num_nonempty_lines": {
    "base": 31,
    "ft": 25
  },
  "uses_allocatable": {
    "base": false,
    "ft": true
  },
  "uses_allocate": {
    "base": false,
    "ft": true
  },
  "uses_assumed_shape": {
    "base": false,
    "ft": true
  },
  "uses_hardcoded_arrays": {
    "base": false,
    "ft": true
  },
  "uses_read_stdin": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program find_closest
    implicit none
    integer, parameter :: max_len = 100
    integer :: n, i, j, min_idx, min_idx2
    real :: numbers(max_len), diff, min_diff
    
    ! Read array length
    read(*, *) n
    
    ! Read array elements
    read(*, *) numbers(1:n)
    
    ! Initialize with first pair
    min_diff = abs(numbers(2) - numbers(1))
    min_idx = 1
    min_idx2 = 2
    
    ! Find the closest pair
    do i = 1, n-1
        do j = i+1, n
            diff = abs(numbers(j) - numbers(i))
            if (diff < min_diff) then
                min_diff = diff
                min_idx = i
                min_idx2 = j
            end if
        end do
    end do
    
    ! Output the closest pair in order (smaller, larger)
    if (numbers(min_idx) < numbers(min_idx2)) then
        print *, numbers(min_idx), numbers(min_idx2)
    else
        print *, numbers(min_idx2), numbers(min_idx)
    end if
    
end program find_closest
```


## FT generated code

```fortran
program main
      implicit none
      integer :: numbers_len
      real, allocatable :: numbers(:)
      integer :: i, j
      real :: min_diff
      integer :: idx1, idx2

      ! Hardcoded input based on the example provided in the prompt
      numbers_len = 6
      allocate(numbers(numbers_len))
      numbers = [1.0, 2.0, 3.0, 4.0, 5.0, 2.2]

      min_diff = huge(0.0)
      idx1 = 1
      idx2 = 2

      do i = 1, numbers_len
        do j = i + 1, numbers_len
          if (abs(numbers(i) - numbers(j)) < min_diff) then
            min_diff = abs(numbers(i) - numbers(j))
            idx1 = i
            idx2 = j
          end if
        end do
      end do

      print *, numbers(min(idx1, idx2)), numbers(max(idx1, idx2))

    end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,37 +1,30 @@
-program find_closest
-    implicit none
-    integer, parameter :: max_len = 100
-    integer :: n, i, j, min_idx, min_idx2
-    real :: numbers(max_len), diff, min_diff
-    
-    ! Read array length
-    read(*, *) n
-    
-    ! Read array elements
-    read(*, *) numbers(1:n)
-    
-    ! Initialize with first pair
-    min_diff = abs(numbers(2) - numbers(1))
-    min_idx = 1
-    min_idx2 = 2
-    
-    ! Find the closest pair
-    do i = 1, n-1
-        do j = i+1, n
-            diff = abs(numbers(j) - numbers(i))
-            if (diff < min_diff) then
-                min_diff = diff
-                min_idx = i
-                min_idx2 = j
-            end if
+program main
+      implicit none
+      integer :: numbers_len
+      real, allocatable :: numbers(:)
+      integer :: i, j
+      real :: min_diff
+      integer :: idx1, idx2
+
+      ! Hardcoded input based on the example provided in the prompt
+      numbers_len = 6
+      allocate(numbers(numbers_len))
+      numbers = [1.0, 2.0, 3.0, 4.0, 5.0, 2.2]
+
+      min_diff = huge(0.0)
+      idx1 = 1
+      idx2 = 2
+
+      do i = 1, numbers_len
+        do j = i + 1, numbers_len
+          if (abs(numbers(i) - numbers(j)) < min_diff) then
+            min_diff = abs(numbers(i) - numbers(j))
+            idx1 = i
+            idx2 = j
+          end if
         end do
-    end do
-    
-    ! Output the closest pair in order (smaller, larger)
-    if (numbers(min_idx) < numbers(min_idx2)) then
-        print *, numbers(min_idx), numbers(min_idx2)
-    else
-        print *, numbers(min_idx2), numbers(min_idx)
-    end if
-    
-end program find_closest
+      end do
+
+      print *, numbers(min(idx1, idx2)), numbers(max(idx1, idx2))
+
+    end program main
```
