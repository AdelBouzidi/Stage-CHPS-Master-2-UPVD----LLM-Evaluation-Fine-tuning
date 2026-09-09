# Failure case: ft_AB_antineighbor_humaneval_mistral_conc20 / task 121

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_stdin_read, status_compile_err`


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
  "has_debug_words": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 32,
    "ft": 23
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 19
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
program main
  implicit none
  integer :: lst_len
  integer, allocatable :: lst(:)
  integer :: result

  ! Read input
  read(*,*) lst_len
  allocate(lst(lst_len))
  read(*,*) lst

  ! Calculate result
  result = 0
  do i = 1, lst_len
    if (mod(i - 1, 2) == 0 .and. mod(lst(i), 2) /= 0) then
      result = result + lst(i)
    end if
  end do

  ! Output result
  print *, result

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,23 @@
-program sum_odd_at_even_positions
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
-end program sum_odd_at_even_positions
+program main
+  implicit none
+  integer :: lst_len
+  integer, allocatable :: lst(:)
+  integer :: result
+
+  ! Read input
+  read(*,*) lst_len
+  allocate(lst(lst_len))
+  read(*,*) lst
+
+  ! Calculate result
+  result = 0
+  do i = 1, lst_len
+    if (mod(i - 1, 2) == 0 .and. mod(lst(i), 2) /= 0) then
+      result = result + lst(i)
+    end if
+  end do
+
+  ! Output result
+  print *, result
+
+end program main
```
