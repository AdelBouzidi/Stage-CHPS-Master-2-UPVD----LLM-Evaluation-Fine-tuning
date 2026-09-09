# Failure case: ft_AB_shuffle_humaneval_mistral_conc15 / task 21

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_output_labels`

- Labels: `static_modifies_intent_in_possible, static_output_labels, status_ineq`


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
  "has_contains": {
    "base": false,
    "ft": true
  },
  "has_debug_words": {
    "base": false,
    "ft": true
  },
  "has_labels_in_output": {
    "base": false,
    "ft": true
  },
  "modifies_intent_in_possible": {
    "base": false,
    "ft": true
  },
  "num_functions": {
    "base": 0,
    "ft": 2
  },
  "num_lines": {
    "base": 33,
    "ft": 46
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 38
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
program rescale_to_unit_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: result(:)
  integer :: i

  ! Hardcoded input data
  numbers_len = 5
  allocate(numbers(numbers_len))
  numbers = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp]

  ! Call the function
  result = rescale_to_unit(numbers_len, numbers)

  ! Output the result
  print *, 'Result:'
  do i = 1, size(result)
    print *, result(i)
  end do

contains

  function rescale_to_unit(numbers_len, numbers) result(res)
    implicit none
    integer, intent(in) :: numbers_len
    real(dp), intent(in) :: numbers(numbers_len)
    real(dp), allocatable :: res(:)
    real(dp) :: min_val, max_val
    integer :: i

    allocate(res(numbers_len))
    min_val = minval(numbers)
    max_val = maxval(numbers)
    
    if (max_val == min_val) then
      res = 0.0_dp
    else
      do i = 1, numbers_len
        res(i) = (numbers(i) - min_val) / (max_val - min_val)
      end do
    end if
  end function rescale_to_unit

end program rescale_to_unit_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,46 @@
-program rescale_to_unit
+program rescale_to_unit_demo
+  implicit none
+  integer, parameter :: dp = kind(1.0d0)
+  integer :: numbers_len
+  real(dp), allocatable :: numbers(:)
+  real(dp), allocatable :: result(:)
+  integer :: i
+
+  ! Hardcoded input data
+  numbers_len = 5
+  allocate(numbers(numbers_len))
+  numbers = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp]
+
+  ! Call the function
+  result = rescale_to_unit(numbers_len, numbers)
+
+  ! Output the result
+  print *, 'Result:'
+  do i = 1, size(result)
+    print *, result(i)
+  end do
+
+contains
+
+  function rescale_to_unit(numbers_len, numbers) result(res)
     implicit none
-    integer :: n_input, i
-    real, allocatable :: numbers(:), rescaled(:)
-    real :: min_val, max_val
+    integer, intent(in) :: numbers_len
+    real(dp), intent(in) :: numbers(numbers_len)
+    real(dp), allocatable :: res(:)
+    real(dp) :: min_val, max_val
+    integer :: i
+
+    allocate(res(numbers_len))
+    min_val = minval(numbers)
+    max_val = maxval(numbers)
     
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
     if (max_val == min_val) then
-        rescaled = 0.0
+      res = 0.0_dp
     else
-        rescaled = (numbers - min_val) / (max_val - min_val)
+      do i = 1, numbers_len
+        res(i) = (numbers(i) - min_val) / (max_val - min_val)
+      end do
     end if
-    
-    ! Output result
-    do i = 1, n_input
-        write(*, '(F8.3)') rescaled(i)
-    end do
-    
-    deallocate(numbers)
-end program rescale_to_unit
+  end function rescale_to_unit
+
+end program rescale_to_unit_demo
```
