# Failure case: ft_B_humaneval_mistral_conc20 / task 20

- Base status: `ok`

- FT status: `runtime_err`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_stdin_read, status_runtime_err`


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
    "ft": 45
  },
  "num_nonempty_lines": {
    "base": 31,
    "ft": 38
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
  "uses_print_star": {
    "base": true,
    "ft": false
  },
  "uses_write_star": {
    "base": false,
    "ft": true
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
program find_closest
  implicit none
  integer :: n
  real, allocatable :: numbers(:)
  integer :: i, j, min_idx, min_idx2
  real :: min_diff, diff
  real :: result1, result2

  ! Read input
  read(*,*) n
  allocate(numbers(n))
  do i = 1, n
    read(*,*) numbers(i)
  end do

  ! Find the two closest elements
  min_diff = 1.0e30
  min_idx = 1
  min_idx2 = 2

  do i = 1, n
    do j = i + 1, n
      diff = abs(numbers(i) - numbers(j))
      if (diff < min_diff) then
        min_diff = diff
        min_idx = i
        min_idx2 = j
      end if
    end do
  end do

  ! Output the two closest elements in order
  if (numbers(min_idx) < numbers(min_idx2)) then
    result1 = numbers(min_idx)
    result2 = numbers(min_idx2)
  else
    result1 = numbers(min_idx2)
    result2 = numbers(min_idx)
  end if

  write(*,*) result1, result2

  deallocate(numbers)

end program find_closest
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,37 +1,45 @@
 program find_closest
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
-        end do
+  implicit none
+  integer :: n
+  real, allocatable :: numbers(:)
+  integer :: i, j, min_idx, min_idx2
+  real :: min_diff, diff
+  real :: result1, result2
+
+  ! Read input
+  read(*,*) n
+  allocate(numbers(n))
+  do i = 1, n
+    read(*,*) numbers(i)
+  end do
+
+  ! Find the two closest elements
+  min_diff = 1.0e30
+  min_idx = 1
+  min_idx2 = 2
+
+  do i = 1, n
+    do j = i + 1, n
+      diff = abs(numbers(i) - numbers(j))
+      if (diff < min_diff) then
+        min_diff = diff
+        min_idx = i
+        min_idx2 = j
+      end if
     end do
-    
-    ! Output the closest pair in order (smaller, larger)
-    if (numbers(min_idx) < numbers(min_idx2)) then
-        print *, numbers(min_idx), numbers(min_idx2)
-    else
-        print *, numbers(min_idx2), numbers(min_idx)
-    end if
-    
+  end do
+
+  ! Output the two closest elements in order
+  if (numbers(min_idx) < numbers(min_idx2)) then
+    result1 = numbers(min_idx)
+    result2 = numbers(min_idx2)
+  else
+    result1 = numbers(min_idx2)
+    result2 = numbers(min_idx)
+  end if
+
+  write(*,*) result1, result2
+
+  deallocate(numbers)
+
 end program find_closest
```
