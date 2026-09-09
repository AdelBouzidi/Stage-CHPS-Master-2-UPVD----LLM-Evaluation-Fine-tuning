# Failure case: ft_AC_shuffle_humaneval_mistral_conc3 / task 21

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_output_labels, static_stdin_read, status_ineq`


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
  "has_debug_words": {
    "base": false,
    "ft": true
  },
  "has_labels_in_output": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 33,
    "ft": 29
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 24
  },
  "uses_print_star": {
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
program rescale_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: rescaled(:)
  real(dp) :: min_val, max_val

  ! Read input
  read(*, *) numbers_len
  allocate(numbers(numbers_len))
  read(*, *) numbers

  ! Calculate min and max
  min_val = minval(numbers)
  max_val = maxval(numbers)

  ! Rescale to unit range
  if (max_val > min_val) then
    rescaled = (numbers - min_val) / (max_val - min_val)
  else
    rescaled = 0.0_dp
  end if

  ! Output result
  print *, 'Rescaled values:'
  print *, rescaled

end program rescale_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,29 @@
-program rescale_to_unit
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
+program rescale_demo
+  implicit none
+  integer, parameter :: dp = kind(1.0d0)
+  integer :: numbers_len
+  real(dp), allocatable :: numbers(:)
+  real(dp), allocatable :: rescaled(:)
+  real(dp) :: min_val, max_val
+
+  ! Read input
+  read(*, *) numbers_len
+  allocate(numbers(numbers_len))
+  read(*, *) numbers
+
+  ! Calculate min and max
+  min_val = minval(numbers)
+  max_val = maxval(numbers)
+
+  ! Rescale to unit range
+  if (max_val > min_val) then
+    rescaled = (numbers - min_val) / (max_val - min_val)
+  else
+    rescaled = 0.0_dp
+  end if
+
+  ! Output result
+  print *, 'Rescaled values:'
+  print *, rescaled
+
+end program rescale_demo
```
