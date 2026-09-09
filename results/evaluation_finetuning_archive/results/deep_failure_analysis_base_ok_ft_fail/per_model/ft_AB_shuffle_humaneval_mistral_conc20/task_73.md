# Failure case: ft_AB_shuffle_humaneval_mistral_conc20 / task 73

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
  "has_debug_words": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 29,
    "ft": 24
  },
  "num_nonempty_lines": {
    "base": 22,
    "ft": 20
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
program palindrome_change
  implicit none
  integer :: arr_len, i, result
  integer, allocatable :: arr(:)

  ! Read input
  read(*,*) arr_len
  allocate(arr(arr_len))
  do i = 1, arr_len
    read(*,*) arr(i)
  end do

  ! Calculate minimum changes needed to make array palindromic
  result = 0
  do i = 1, arr_len/2
    if (arr(i) /= arr(arr_len - i + 1)) then
      result = result + 1
    end if
  end do

  ! Output result
  print *, result

end program palindrome_change
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,29 +1,24 @@
-program palindrome_changes
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
-end program palindrome_changes
+program palindrome_change
+  implicit none
+  integer :: arr_len, i, result
+  integer, allocatable :: arr(:)
+
+  ! Read input
+  read(*,*) arr_len
+  allocate(arr(arr_len))
+  do i = 1, arr_len
+    read(*,*) arr(i)
+  end do
+
+  ! Calculate minimum changes needed to make array palindromic
+  result = 0
+  do i = 1, arr_len/2
+    if (arr(i) /= arr(arr_len - i + 1)) then
+      result = result + 1
+    end if
+  end do
+
+  ! Output result
+  print *, result
+
+end program palindrome_change
```
