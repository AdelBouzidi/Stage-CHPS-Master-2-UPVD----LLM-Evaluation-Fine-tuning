# Failure case: ft_C_humaneval_mistral_conc3 / task 20

- Base status: `ok`

- FT status: `runtime_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_runtime_err`


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
    "ft": 39
  },
  "num_nonempty_lines": {
    "base": 31,
    "ft": 33
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
  integer :: n, i, j, min_idx, min_idx2
  real :: numbers(1000), min_diff, diff
  integer :: idx1, idx2

  ! Read the number of elements
  read(*, *) n

  ! Read the array elements
  do i = 1, n
    read(*, *) numbers(i)
  end do

  ! Initialize minimum difference with first pair
  min_diff = abs(numbers(2) - numbers(1))
  idx1 = 1
  idx2 = 2

  ! Find the pair with minimum difference
  do i = 1, n-1
    do j = i+1, n
      diff = abs(numbers(j) - numbers(i))
      if (diff < min_diff) then
        min_diff = diff
        idx1 = i
        idx2 = j
      end if
    end do
  end do

  ! Output the two closest numbers in order
  if (numbers(idx1) < numbers(idx2)) then
    print *, numbers(idx1), numbers(idx2)
  else
    print *, numbers(idx2), numbers(idx1)
  end if

end program find_closest
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,37 +1,39 @@
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
+  integer :: n, i, j, min_idx, min_idx2
+  real :: numbers(1000), min_diff, diff
+  integer :: idx1, idx2
+
+  ! Read the number of elements
+  read(*, *) n
+
+  ! Read the array elements
+  do i = 1, n
+    read(*, *) numbers(i)
+  end do
+
+  ! Initialize minimum difference with first pair
+  min_diff = abs(numbers(2) - numbers(1))
+  idx1 = 1
+  idx2 = 2
+
+  ! Find the pair with minimum difference
+  do i = 1, n-1
+    do j = i+1, n
+      diff = abs(numbers(j) - numbers(i))
+      if (diff < min_diff) then
+        min_diff = diff
+        idx1 = i
+        idx2 = j
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
+  ! Output the two closest numbers in order
+  if (numbers(idx1) < numbers(idx2)) then
+    print *, numbers(idx1), numbers(idx2)
+  else
+    print *, numbers(idx2), numbers(idx1)
+  end if
+
 end program find_closest
```
