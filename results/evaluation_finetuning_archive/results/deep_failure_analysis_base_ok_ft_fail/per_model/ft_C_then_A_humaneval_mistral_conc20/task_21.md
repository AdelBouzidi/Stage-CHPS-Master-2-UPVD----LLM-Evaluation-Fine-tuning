# Failure case: ft_C_then_A_humaneval_mistral_conc20 / task 21

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
  "modifies_intent_in_possible": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 33,
    "ft": 36
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 31
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
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
program rescale_to_unit
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: res(:)
  
  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  read(*,*) numbers
  
  ! Call the function
  call rescale_to_unit(numbers_len, numbers, res)
  
  ! Output results
  print *, numbers_len
  print *, res
contains
  subroutine rescale_to_unit(numbers_len, numbers, res)
    implicit none
    integer, intent(in) :: numbers_len
    real(dp), intent(in) :: numbers(numbers_len)
    real(dp), intent(out) :: res(numbers_len)
    real(dp) :: min_val, max_val
    
    min_val = minval(numbers)
    max_val = maxval(numbers)
    
    if (max_val == min_val) then
      res = 0.0_dp
    else
      res = (numbers - min_val) / (max_val - min_val)
    end if
  end subroutine rescale_to_unit
end program rescale_to_unit
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,36 @@
 program rescale_to_unit
+  implicit none
+  integer, parameter :: dp = kind(1.0d0)
+  integer :: numbers_len
+  real(dp), allocatable :: numbers(:)
+  real(dp), allocatable :: res(:)
+  
+  ! Read input
+  read(*,*) numbers_len
+  allocate(numbers(numbers_len))
+  read(*,*) numbers
+  
+  ! Call the function
+  call rescale_to_unit(numbers_len, numbers, res)
+  
+  ! Output results
+  print *, numbers_len
+  print *, res
+contains
+  subroutine rescale_to_unit(numbers_len, numbers, res)
     implicit none
-    integer :: n_input, i
-    real, allocatable :: numbers(:), rescaled(:)
-    real :: min_val, max_val
+    integer, intent(in) :: numbers_len
+    real(dp), intent(in) :: numbers(numbers_len)
+    real(dp), intent(out) :: res(numbers_len)
+    real(dp) :: min_val, max_val
     
-    ! Read input
-    read(*,*) n_input
-    allocate(numbers(n_input))
-    read(*,*) numbers
+    min_val = minval(numbers)
+    max_val = maxval(numbers)
     
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
+      res = (numbers - min_val) / (max_val - min_val)
     end if
-    
-    ! Output result
-    do i = 1, n_input
-        write(*, '(F8.3)') rescaled(i)
-    end do
-    
-    deallocate(numbers)
+  end subroutine rescale_to_unit
 end program rescale_to_unit
```
