# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 21

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_output_labels, status_compile_err`


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
  "has_labels_in_output": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 33,
    "ft": 20
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 20
  },
  "uses_allocate": {
    "base": true,
    "ft": false
  },
  "uses_hardcoded_arrays": {
    "base": false,
    "ft": true
  },
  "uses_print_star": {
    "base": false,
    "ft": true
  },
  "uses_read_stdin": {
    "base": true,
    "ft": false
  },
  "uses_write_star": {
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
            integer :: numbers_len
            real :: numbers(10)
            real :: res
            real, allocatable :: rescale(:)
            real :: numbers_in(10)
            real :: numbers_out(10)
            integer :: i
            !
            numbers_len = 5
            numbers = (/ 1.0, 2.0, 3.0, 4.0, 5.0 /)
            !
            rescale = rescale_to_unit(numbers_len, numbers)
            !
            print *, 'rescale_to_unit'
            print *, numbers_len
            print *, rescale
            !
            end program rescale_to_unit
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,20 @@
 program rescale_to_unit
-    implicit none
-    integer :: n_input, i
-    real, allocatable :: numbers(:), rescaled(:)
-    real :: min_val, max_val
-    
-    ! Read input
-    read(*,*) n_input
-    allocate(numbers(n_input))
-    read(*,*) numbers
-    
-    ! Find min and max
-    min_val = numbers(1)
-    max_val = numbers(1)
-    do i = 2, n_input
-        if (numbers(i) < min_val) min_val = numbers(i)
-        if (numbers(i) > max_val) max_val = numbers(i)
-    end do
-    
-    ! Apply linear transform
-    if (max_val == min_val) then
-        rescaled = 0.0
-    else
-        rescaled = (numbers - min_val) / (max_val - min_val)
-    end if
-    
-    ! Output result
-    do i = 1, n_input
-        write(*, '(F8.3)') rescaled(i)
-    end do
-    
-    deallocate(numbers)
-end program rescale_to_unit
+            implicit none
+            integer :: numbers_len
+            real :: numbers(10)
+            real :: res
+            real, allocatable :: rescale(:)
+            real :: numbers_in(10)
+            real :: numbers_out(10)
+            integer :: i
+            !
+            numbers_len = 5
+            numbers = (/ 1.0, 2.0, 3.0, 4.0, 5.0 /)
+            !
+            rescale = rescale_to_unit(numbers_len, numbers)
+            !
+            print *, 'rescale_to_unit'
+            print *, numbers_len
+            print *, rescale
+            !
+            end program rescale_to_unit
```
