# Failure case: ft_B_humaneval_mistral_conc3 / task 73

- Base status: `ok`

- FT status: `runtime_err`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_stdin_read, status_runtime_err`


## Prompt

```text
Write a Fortran90 program that given an array of integers, finds the minimum number of elements that need to be changed to make the array palindromic.
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
    "base": 29,
    "ft": 30
  },
  "num_nonempty_lines": {
    "base": 22,
    "ft": 24
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
program palindrome_changes
    implicit none
    integer :: n, i, count
    integer, allocatable :: arr(:)
    
    ! Read array length
    read *, n
    
    ! Allocate array
    allocate(arr(n))
    
    ! Read array elements
    read *, arr
    
    ! Count mismatches for palindrome
    count = 0
    do i = 1, n/2
        if (arr(i) /= arr(n - i + 1)) then
            count = count + 1
        end if
    end do
    
    ! Output result
    write (*, *) count
    
    ! Deallocate
    deallocate(arr)
    
end program palindrome_changes
```


## FT generated code

```fortran
program palindrome_changes
  implicit none
  integer, parameter :: max_len = 1000
  integer :: arr_len
  integer, allocatable :: arr(:)
  integer :: i, changes
  
  ! Read array length
  read(*,*) arr_len
  
  ! Read array elements
  allocate(arr(arr_len))
  do i = 1, arr_len
    read(*,*) arr(i)
  end do
  
  ! Count changes needed
  changes = 0
  do i = 1, arr_len/2
    if (arr(i) /= arr(arr_len - i + 1)) then
      changes = changes + 1
    end if
  end do
  
  ! Output result
  print*, changes
  
  deallocate(arr)
  
end program palindrome_changes
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,29 +1,30 @@
 program palindrome_changes
-    implicit none
-    integer :: n, i, count
-    integer, allocatable :: arr(:)
-    
-    ! Read array length
-    read *, n
-    
-    ! Allocate array
-    allocate(arr(n))
-    
-    ! Read array elements
-    read *, arr
-    
-    ! Count mismatches for palindrome
-    count = 0
-    do i = 1, n/2
-        if (arr(i) /= arr(n - i + 1)) then
-            count = count + 1
-        end if
-    end do
-    
-    ! Output result
-    write (*, *) count
-    
-    ! Deallocate
-    deallocate(arr)
-    
+  implicit none
+  integer, parameter :: max_len = 1000
+  integer :: arr_len
+  integer, allocatable :: arr(:)
+  integer :: i, changes
+  
+  ! Read array length
+  read(*,*) arr_len
+  
+  ! Read array elements
+  allocate(arr(arr_len))
+  do i = 1, arr_len
+    read(*,*) arr(i)
+  end do
+  
+  ! Count changes needed
+  changes = 0
+  do i = 1, arr_len/2
+    if (arr(i) /= arr(arr_len - i + 1)) then
+      changes = changes + 1
+    end if
+  end do
+  
+  ! Output result
+  print*, changes
+  
+  deallocate(arr)
+  
 end program palindrome_changes
```
