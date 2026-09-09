# Failure case: ft_AC_antineighbor_humaneval_mistral_conc20 / task 21

- Base status: `ok`

- FT status: `runtime_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_runtime_err`


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
  "modifies_intent_in_possible": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 33,
    "ft": 47
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 38
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
program rescale_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: n
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: rescaled(:)
  integer :: i

  ! Read input
  read(*,*) n
  allocate(numbers(n))
  read(*,*) numbers

  ! Call the rescale function
  call rescale_to_unit(n, numbers, rescaled)

  ! Output result
  print *, rescaled

contains

  subroutine rescale_to_unit(n, numbers, rescaled)
    implicit none
    integer, intent(in) :: n
    real(dp), intent(in) :: numbers(n)
    real(dp), intent(out) :: rescaled(n)
    real(dp) :: min_val, max_val, range

    min_val = numbers(1)
    do i = 2, n
      if (numbers(i) < min_val) min_val = numbers(i)
    end do

    max_val = numbers(1)
    do i = 2, n
      if (numbers(i) > max_val) max_val = numbers(i)
    end do

    range = max_val - min_val
    if (range == 0.0_dp) then
      rescaled = 0.0_dp
    else
      rescaled = (numbers - min_val) / range
    end if
  end subroutine rescale_to_unit

end program rescale_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,47 @@
-program rescale_to_unit
+program rescale_demo
+  implicit none
+  integer, parameter :: dp = kind(1.0d0)
+  integer :: n
+  real(dp), allocatable :: numbers(:)
+  real(dp), allocatable :: rescaled(:)
+  integer :: i
+
+  ! Read input
+  read(*,*) n
+  allocate(numbers(n))
+  read(*,*) numbers
+
+  ! Call the rescale function
+  call rescale_to_unit(n, numbers, rescaled)
+
+  ! Output result
+  print *, rescaled
+
+contains
+
+  subroutine rescale_to_unit(n, numbers, rescaled)
     implicit none
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
+    integer, intent(in) :: n
+    real(dp), intent(in) :: numbers(n)
+    real(dp), intent(out) :: rescaled(n)
+    real(dp) :: min_val, max_val, range
+
     min_val = numbers(1)
+    do i = 2, n
+      if (numbers(i) < min_val) min_val = numbers(i)
+    end do
+
     max_val = numbers(1)
-    do i = 2, n_input
-        if (numbers(i) < min_val) min_val = numbers(i)
-        if (numbers(i) > max_val) max_val = numbers(i)
+    do i = 2, n
+      if (numbers(i) > max_val) max_val = numbers(i)
     end do
-    
-    ! Apply linear transform
-    if (max_val == min_val) then
-        rescaled = 0.0
+
+    range = max_val - min_val
+    if (range == 0.0_dp) then
+      rescaled = 0.0_dp
     else
-        rescaled = (numbers - min_val) / (max_val - min_val)
+      rescaled = (numbers - min_val) / range
     end if
-    
-    ! Output result
-    do i = 1, n_input
-        write(*, '(F8.3)') rescaled(i)
-    end do
-    
-    deallocate(numbers)
-end program rescale_to_unit
+  end subroutine rescale_to_unit
+
+end program rescale_demo
```
