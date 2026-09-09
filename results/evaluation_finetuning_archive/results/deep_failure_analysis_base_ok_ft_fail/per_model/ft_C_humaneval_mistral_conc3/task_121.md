# Failure case: ft_C_humaneval_mistral_conc3 / task 121

- Base status: `ok`

- FT status: `runtime_err`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_stdin_read, status_runtime_err`


## Prompt

```text
Write a Fortran90 program that returns the sum of all odd elements at even positions in the given non-empty array of integers.
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
    "base": 32,
    "ft": 27
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 22
  },
  "uses_index_0_loop": {
    "base": true,
    "ft": false
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
program sum_odd_at_even_positions
    implicit none
    integer :: n
    integer, allocatable :: lst(:)
    integer :: i
    integer :: sum = 0
    
    ! Read array length
    read *, n
    
    ! Allocate array
    allocate(lst(n))
    
    ! Read array elements
    read *, lst
    
    ! Calculate sum of odd elements at even positions (0-indexed)
    sum = 0
    do i = 0, n-1
        if (mod(i, 2) == 0) then  ! even position (0-indexed)
            if (mod(lst(i+1), 2) /= 0) then  ! odd value
                sum = sum + lst(i+1)
            end if
        end if
    end do
    
    ! Output result
    write (*, *) sum
    
    ! Deallocate
    deallocate(lst)
end program sum_odd_at_even_positions
```


## FT generated code

```fortran
program sum_odd_at_even_positions
  implicit none
  integer :: n, i, sum, value
  integer, allocatable :: arr(:)
  
  ! Read array length
  read(*, *) n
  
  ! Read array elements
  allocate(arr(n))
  do i = 1, n
    read(*, *) arr(i)
  end do
  
  ! Calculate sum of odd elements at even positions
  sum = 0
  do i = 2, n, 2  ! Even positions: 2, 4, 6, ...
    if (mod(arr(i), 2) /= 0) then  ! Odd value
      sum = sum + arr(i)
    end if
  end do
  
  ! Output result
  print *, sum
  
  deallocate(arr)
end program sum_odd_at_even_positions
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,27 @@
 program sum_odd_at_even_positions
-    implicit none
-    integer :: n
-    integer, allocatable :: lst(:)
-    integer :: i
-    integer :: sum = 0
-    
-    ! Read array length
-    read *, n
-    
-    ! Allocate array
-    allocate(lst(n))
-    
-    ! Read array elements
-    read *, lst
-    
-    ! Calculate sum of odd elements at even positions (0-indexed)
-    sum = 0
-    do i = 0, n-1
-        if (mod(i, 2) == 0) then  ! even position (0-indexed)
-            if (mod(lst(i+1), 2) /= 0) then  ! odd value
-                sum = sum + lst(i+1)
-            end if
-        end if
-    end do
-    
-    ! Output result
-    write (*, *) sum
-    
-    ! Deallocate
-    deallocate(lst)
+  implicit none
+  integer :: n, i, sum, value
+  integer, allocatable :: arr(:)
+  
+  ! Read array length
+  read(*, *) n
+  
+  ! Read array elements
+  allocate(arr(n))
+  do i = 1, n
+    read(*, *) arr(i)
+  end do
+  
+  ! Calculate sum of odd elements at even positions
+  sum = 0
+  do i = 2, n, 2  ! Even positions: 2, 4, 6, ...
+    if (mod(arr(i), 2) /= 0) then  ! Odd value
+      sum = sum + arr(i)
+    end if
+  end do
+  
+  ! Output result
+  print *, sum
+  
+  deallocate(arr)
 end program sum_odd_at_even_positions
```
