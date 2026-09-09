# Failure case: ft_ABC_Strong_humaneval_mistral_conc3 / task 20

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_c_like_signature`

- Labels: `static_c_like_signature, static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
  "has_debug_words": {
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
  "uses_c_like_signature": {
    "base": false,
    "ft": true
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
program find_closest_elements_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp) :: result1, result2

  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  read(*,*) numbers

  ! Call the function
  call find_closest_elements(numbers_len, numbers, result1, result2)

  ! Output result
  print *, result1, result2

contains

  subroutine find_closest_elements(int numbers_len, float numbers, float result1, float result2)
    implicit none
    integer, intent(in) :: numbers_len
    real(dp), intent(in) :: numbers(:)
    real(dp), intent(out) :: result1, result2
    integer :: i, j, min_idx, min_j
    real(dp) :: min_diff, diff

    min_diff = huge(0.0_dp)
    min_idx = 0
    min_j = 0

    do i = 1, numbers_len
      do j = i + 1, numbers_len
        diff = abs(numbers(i) - numbers(j))
        if (diff < min_diff) then
          min_diff = diff
          min_idx = i
          min_j = j
        end if
      end do
    end do

    if (numbers(min_idx) < numbers(min_j)) then
      result1 = numbers(min_idx)
      result2 = numbers(min_j)
    else
      result1 = numbers(min_j)
      result2 = numbers(min_idx)
    end if
  end subroutine find_closest_elements

end program find_closest_elements_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,37 +1,53 @@
-program find_closest
+program find_closest_elements_demo
+  implicit none
+  integer, parameter :: dp = kind(1.0d0)
+  integer :: numbers_len
+  real(dp), allocatable :: numbers(:)
+  real(dp) :: result1, result2
+
+  ! Read input
+  read(*,*) numbers_len
+  allocate(numbers(numbers_len))
+  read(*,*) numbers
+
+  ! Call the function
+  call find_closest_elements(numbers_len, numbers, result1, result2)
+
+  ! Output result
+  print *, result1, result2
+
+contains
+
+  subroutine find_closest_elements(int numbers_len, float numbers, float result1, float result2)
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
+    real(dp), intent(in) :: numbers(:)
+    real(dp), intent(out) :: result1, result2
+    integer :: i, j, min_idx, min_j
+    real(dp) :: min_diff, diff
+
+    min_diff = huge(0.0_dp)
+    min_idx = 0
+    min_j = 0
+
+    do i = 1, numbers_len
+      do j = i + 1, numbers_len
+        diff = abs(numbers(i) - numbers(j))
+        if (diff < min_diff) then
+          min_diff = diff
+          min_idx = i
+          min_j = j
+        end if
+      end do
     end do
-    
-    ! Output the closest pair in order (smaller, larger)
-    if (numbers(min_idx) < numbers(min_idx2)) then
-        print *, numbers(min_idx), numbers(min_idx2)
+
+    if (numbers(min_idx) < numbers(min_j)) then
+      result1 = numbers(min_idx)
+      result2 = numbers(min_j)
     else
-        print *, numbers(min_idx2), numbers(min_idx)
+      result1 = numbers(min_j)
+      result2 = numbers(min_idx)
     end if
-    
-end program find_closest
+  end subroutine find_closest_elements
+
+end program find_closest_elements_demo
```
