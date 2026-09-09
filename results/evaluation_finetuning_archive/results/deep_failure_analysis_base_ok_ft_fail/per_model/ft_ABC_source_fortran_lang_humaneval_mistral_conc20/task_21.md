# Failure case: ft_ABC_source_fortran_lang_humaneval_mistral_conc20 / task 21

- Base status: `ok`

- FT status: `runtime_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_runtime_err`


## Prompt

```text
Write a Fortran90 program that given an array of numbers (of at least two elements), applies a linear transform to that array, such that the smallest number will become 0 and the largest will become 1.
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
    "base": 33,
    "ft": 39
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 34
  },
  "uses_allocatable": {
    "base": true,
    "ft": false
  },
  "uses_allocate": {
    "base": true,
    "ft": false
  },
  "uses_assumed_shape": {
    "base": true,
    "ft": false
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program rescale_to_unit
    implicit none
    integer :: n_input, i
    real, allocatable :: numbers(:), rescaled(:)
    real :: min_val, max_val
    
    ! Read input
    read(*,*) n_input
    allocate(numbers(n_input))
    read(*,*) numbers
    
    ! Find min and max
    min_val = numbers(1)
    max_val = numbers(1)
    do i = 2, n_input
        if (numbers(i) < min_val) min_val = numbers(i)
        if (numbers(i) > max_val) max_val = numbers(i)
    end do
    
    ! Apply linear transform
    if (max_val == min_val) then
        rescaled = 0.0
    else
        rescaled = (numbers - min_val) / (max_val - min_val)
    end if
    
    ! Output result
    do i = 1, n_input
        write(*, '(F8.3)') rescaled(i)
    end do
    
    deallocate(numbers)
end program rescale_to_unit
```


## FT generated code

```fortran
program rescale_to_unit
    implicit none
    integer, parameter :: max_len = 100
    integer :: n
    real, dimension(max_len) :: numbers
    real :: min_val, max_val
    real :: rescaled
    integer :: i
    
    ! Read number of elements
    read(*,*) n
    
    ! Read the array elements
    do i = 1, n
        read(*,*) numbers(i)
    end do
    
    ! Find min and max
    min_val = numbers(1)
    max_val = numbers(1)
    do i = 2, n
        if (numbers(i) < min_val) min_val = numbers(i)
        if (numbers(i) > max_val) max_val = numbers(i)
    end do
    
    ! Apply linear transform
    if (max_val == min_val) then
        ! All values are the same, output zeros
        do i = 1, n
            write(*,*) 0.0
        end do
    else
        do i = 1, n
            rescaled = (numbers(i) - min_val) / (max_val - min_val)
            write(*,*) rescaled
        end do
    end if
    
end program rescale_to_unit
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,39 @@
 program rescale_to_unit
     implicit none
-    integer :: n_input, i
-    real, allocatable :: numbers(:), rescaled(:)
+    integer, parameter :: max_len = 100
+    integer :: n
+    real, dimension(max_len) :: numbers
     real :: min_val, max_val
+    real :: rescaled
+    integer :: i
     
-    ! Read input
-    read(*,*) n_input
-    allocate(numbers(n_input))
-    read(*,*) numbers
+    ! Read number of elements
+    read(*,*) n
+    
+    ! Read the array elements
+    do i = 1, n
+        read(*,*) numbers(i)
+    end do
     
     ! Find min and max
     min_val = numbers(1)
     max_val = numbers(1)
-    do i = 2, n_input
+    do i = 2, n
         if (numbers(i) < min_val) min_val = numbers(i)
         if (numbers(i) > max_val) max_val = numbers(i)
     end do
     
     ! Apply linear transform
     if (max_val == min_val) then
-        rescaled = 0.0
+        ! All values are the same, output zeros
+        do i = 1, n
+            write(*,*) 0.0
+        end do
     else
-        rescaled = (numbers - min_val) / (max_val - min_val)
+        do i = 1, n
+            rescaled = (numbers(i) - min_val) / (max_val - min_val)
+            write(*,*) rescaled
+        end do
     end if
     
-    ! Output result
-    do i = 1, n_input
-        write(*, '(F8.3)') rescaled(i)
-    end do
-    
-    deallocate(numbers)
 end program rescale_to_unit
```
