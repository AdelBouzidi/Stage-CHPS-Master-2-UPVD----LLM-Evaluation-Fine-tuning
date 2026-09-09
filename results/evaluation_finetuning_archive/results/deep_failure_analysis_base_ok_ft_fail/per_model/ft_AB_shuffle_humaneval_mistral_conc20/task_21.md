# Failure case: ft_AB_shuffle_humaneval_mistral_conc20 / task 21

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_stdin_read, status_ok`


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
  "num_lines": {
    "base": 33,
    "ft": 26
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 22
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
program rescale_to_unit_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: res(:)
  real(dp) :: min_val, max_val

  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  read(*,*) numbers

  ! Rescale to unit interval
  min_val = minval(numbers)
  max_val = maxval(numbers)
  if (max_val == min_val) then
    res = 0.0_dp
  else
    res = (numbers - min_val) / (max_val - min_val)
  end if

  ! Output result
  print *, res

end program rescale_to_unit_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,26 @@
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
+program rescale_to_unit_demo
+  implicit none
+  integer, parameter :: dp = kind(1.0d0)
+  integer :: numbers_len
+  real(dp), allocatable :: numbers(:)
+  real(dp), allocatable :: res(:)
+  real(dp) :: min_val, max_val
+
+  ! Read input
+  read(*,*) numbers_len
+  allocate(numbers(numbers_len))
+  read(*,*) numbers
+
+  ! Rescale to unit interval
+  min_val = minval(numbers)
+  max_val = maxval(numbers)
+  if (max_val == min_val) then
+    res = 0.0_dp
+  else
+    res = (numbers - min_val) / (max_val - min_val)
+  end if
+
+  ! Output result
+  print *, res
+
+end program rescale_to_unit_demo
```
