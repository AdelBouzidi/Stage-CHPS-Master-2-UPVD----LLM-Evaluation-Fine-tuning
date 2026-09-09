# Failure case: ft_C_then_A_humaneval_mistral_conc20 / task 121

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


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
  "num_functions": {
    "base": 0,
    "ft": 2
  },
  "num_lines": {
    "base": 32,
    "ft": 33
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 27
  },
  "uses_hardcoded_arrays": {
    "base": false,
    "ft": true
  },
  "uses_index_0_loop": {
    "base": true,
    "ft": false
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
program solution
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: lst_len
  integer, allocatable :: lst(:)
  integer :: result

  ! Hardcoded input as per example
  lst_len = 4
  allocate(lst(lst_len))
  lst = [5, 8, 7, 1]

  result = solution(lst_len, lst)

  print *, result

contains

  integer function solution(lst_len, lst)
    integer, intent(in) :: lst_len
    integer, intent(in) :: lst(:)
    integer :: i
    integer :: sum_val
    sum_val = 0
    do i = 2, lst_len, 2
      if (mod(lst(i), 2) == 1) then
        sum_val = sum_val + lst(i)
      end if
    end do
    solution = sum_val
  end function solution

end program solution
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,33 @@
-program sum_odd_at_even_positions
-    implicit none
-    integer :: n
-    integer, allocatable :: lst(:)
+program solution
+  implicit none
+  integer, parameter :: dp = kind(1.0d0)
+  integer :: lst_len
+  integer, allocatable :: lst(:)
+  integer :: result
+
+  ! Hardcoded input as per example
+  lst_len = 4
+  allocate(lst(lst_len))
+  lst = [5, 8, 7, 1]
+
+  result = solution(lst_len, lst)
+
+  print *, result
+
+contains
+
+  integer function solution(lst_len, lst)
+    integer, intent(in) :: lst_len
+    integer, intent(in) :: lst(:)
     integer :: i
-    integer :: sum = 0
-    
-    ! Read array length
-    read *, n
-    
-    ! Allocate array
-    allocate(lst(n))
-    
-    ! Read array elements
-    read *, lst
-    
-    ! Calculate sum of odd elements at even positions (0-indexed)
-    sum = 0
-    do i = 0, n-1
-        if (mod(i, 2) == 0) then  ! even position (0-indexed)
-            if (mod(lst(i+1), 2) /= 0) then  ! odd value
-                sum = sum + lst(i+1)
-            end if
-        end if
+    integer :: sum_val
+    sum_val = 0
+    do i = 2, lst_len, 2
+      if (mod(lst(i), 2) == 1) then
+        sum_val = sum_val + lst(i)
+      end if
     end do
-    
-    ! Output result
-    write (*, *) sum
-    
-    ! Deallocate
-    deallocate(lst)
-end program sum_odd_at_even_positions
+    solution = sum_val
+  end function solution
+
+end program solution
```
