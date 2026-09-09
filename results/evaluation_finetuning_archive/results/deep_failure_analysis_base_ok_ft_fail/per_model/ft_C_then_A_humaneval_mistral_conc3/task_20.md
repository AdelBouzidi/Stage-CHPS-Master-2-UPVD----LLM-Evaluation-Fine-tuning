# Failure case: ft_C_then_A_humaneval_mistral_conc3 / task 20

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


## Prompt

```text
Write a Fortran90 program that from a supplied array of numbers (of length at least two) select and return two that are the closest to each other and return them in order (smaller number, larger number).
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
    "base": 37,
    "ft": 53
  },
  "num_nonempty_lines": {
    "base": 31,
    "ft": 44
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
  },
  "uses_allocatable": {
    "base": false,
    "ft": true
  },
  "uses_allocate": {
    "base": false,
    "ft": true
  },
  "uses_assumed_shape": {
    "base": false,
    "ft": true
  },
  "uses_hardcoded_arrays": {
    "base": false,
    "ft": true
  },
  "uses_read_stdin": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program find_closest
    implicit none
    integer, parameter :: max_len = 100
    integer :: n, i, j, min_idx, min_idx2
    real :: numbers(max_len), diff, min_diff
    
    ! Read array length
    read(*, *) n
    
    ! Read array elements
    read(*, *) numbers(1:n)
    
    ! Initialize with first pair
    min_diff = abs(numbers(2) - numbers(1))
    min_idx = 1
    min_idx2 = 2
    
    ! Find the closest pair
    do i = 1, n-1
        do j = i+1, n
            diff = abs(numbers(j) - numbers(i))
            if (diff < min_diff) then
                min_diff = diff
                min_idx = i
                min_idx2 = j
            end if
        end do
    end do
    
    ! Output the closest pair in order (smaller, larger)
    if (numbers(min_idx) < numbers(min_idx2)) then
        print *, numbers(min_idx), numbers(min_idx2)
    else
        print *, numbers(min_idx2), numbers(min_idx)
    end if
    
end program find_closest
```


## FT generated code

```fortran
program find_closest_elements
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp) :: result1, result2

  ! Hardcoded input as per example
  numbers_len = 6
  allocate(numbers(numbers_len))
  numbers = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 2.2_dp]

  call find_closest_elements(numbers_len, numbers, result1, result2)

  print *, result1, result2

contains

  subroutine find_closest_elements(numbers_len, numbers, result1, result2)
    implicit none
    integer, intent(in) :: numbers_len
    real(dp), intent(in) :: numbers(numbers_len)
    real(dp), intent(out) :: result1, result2
    integer :: i, j
    real(dp) :: min_diff
    real(dp) :: diff
    integer :: idx1, idx2

    min_diff = huge(min_diff)
    idx1 = 1
    idx2 = 2

    do i = 1, numbers_len - 1
      do j = i + 1, numbers_len
        diff = abs(numbers(i) - numbers(j))
        if (diff < min_diff) then
          min_diff = diff
          idx1 = i
          idx2 = j
        end if
      end do
    end do

    if (numbers(idx1) < numbers(idx2)) then
      result1 = numbers(idx1)
      result2 = numbers(idx2)
    else
      result1 = numbers(idx2)
      result2 = numbers(idx1)
    end if
  end subroutine find_closest_elements

end program find_closest_elements
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,37 +1,53 @@
-program find_closest
+program find_closest_elements
+  implicit none
+  integer, parameter :: dp = kind(1.0d0)
+  integer :: numbers_len
+  real(dp), allocatable :: numbers(:)
+  real(dp) :: result1, result2
+
+  ! Hardcoded input as per example
+  numbers_len = 6
+  allocate(numbers(numbers_len))
+  numbers = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 2.2_dp]
+
+  call find_closest_elements(numbers_len, numbers, result1, result2)
+
+  print *, result1, result2
+
+contains
+
+  subroutine find_closest_elements(numbers_len, numbers, result1, result2)
     implicit none
-    integer, parameter :: max_len = 100
-    integer :: n, i, j, min_idx, min_idx2
-    real :: numbers(max_len), diff, min_diff
-    
-    ! Read array length
-    read(*, *) n
-    
-    ! Read array elements
-    read(*, *) numbers(1:n)
-    
-    ! Initialize with first pair
-    min_diff = abs(numbers(2) - numbers(1))
-    min_idx = 1
-    min_idx2 = 2
-    
-    ! Find the closest pair
-    do i = 1, n-1
-        do j = i+1, n
-            diff = abs(numbers(j) - numbers(i))
-            if (diff < min_diff) then
-                min_diff = diff
-                min_idx = i
-                min_idx2 = j
-            end if
-        end do
+    integer, intent(in) :: numbers_len
+    real(dp), intent(in) :: numbers(numbers_len)
+    real(dp), intent(out) :: result1, result2
+    integer :: i, j
+    real(dp) :: min_diff
+    real(dp) :: diff
+    integer :: idx1, idx2
+
+    min_diff = huge(min_diff)
+    idx1 = 1
+    idx2 = 2
+
+    do i = 1, numbers_len - 1
+      do j = i + 1, numbers_len
+        diff = abs(numbers(i) - numbers(j))
+        if (diff < min_diff) then
+          min_diff = diff
+          idx1 = i
+          idx2 = j
+        end if
+      end do
     end do
-    
-    ! Output the closest pair in order (smaller, larger)
-    if (numbers(min_idx) < numbers(min_idx2)) then
-        print *, numbers(min_idx), numbers(min_idx2)
+
+    if (numbers(idx1) < numbers(idx2)) then
+      result1 = numbers(idx1)
+      result2 = numbers(idx2)
     else
-        print *, numbers(min_idx2), numbers(min_idx)
+      result1 = numbers(idx2)
+      result2 = numbers(idx1)
     end if
-    
-end program find_closest
+  end subroutine find_closest_elements
+
+end program find_closest_elements
```
