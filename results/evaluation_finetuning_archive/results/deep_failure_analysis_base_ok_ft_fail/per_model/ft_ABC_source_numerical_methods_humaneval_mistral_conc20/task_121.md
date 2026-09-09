# Failure case: ft_ABC_source_numerical_methods_humaneval_mistral_conc20 / task 121

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_possible_zero_indexing, status_ok`


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
{}
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
        if (mod(i, 2) == 0) then
            if (mod(lst(i+1), 2) /= 0) then
                sum = sum + lst(i+1)
            end if
        end if
    end do
    
    ! Output result
    write (*, *) sum
    
    ! Deallocate array
    deallocate(lst)
end program sum_odd_at_even_positions
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -17,8 +17,8 @@
     ! Calculate sum of odd elements at even positions (0-indexed)
     sum = 0
     do i = 0, n-1
-        if (mod(i, 2) == 0) then  ! even position (0-indexed)
-            if (mod(lst(i+1), 2) /= 0) then  ! odd value
+        if (mod(i, 2) == 0) then
+            if (mod(lst(i+1), 2) /= 0) then
                 sum = sum + lst(i+1)
             end if
         end if
@@ -27,6 +27,6 @@
     ! Output result
     write (*, *) sum
     
-    ! Deallocate
+    ! Deallocate array
     deallocate(lst)
 end program sum_odd_at_even_positions
```
