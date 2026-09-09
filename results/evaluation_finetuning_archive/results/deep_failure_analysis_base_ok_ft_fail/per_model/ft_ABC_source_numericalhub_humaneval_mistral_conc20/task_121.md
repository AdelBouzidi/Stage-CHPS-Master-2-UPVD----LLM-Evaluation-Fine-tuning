# Failure case: ft_ABC_source_numericalhub_humaneval_mistral_conc20 / task 121

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
  "uses_index_0_loop": {
    "base": true,
    "ft": false
  },
  "uses_print_star": {
    "base": false,
    "ft": true
  },
  "uses_read_stdin": {
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
program test_solution
  implicit none
  integer, parameter :: i4b = selected_int_kind(9)
  integer(i4b) :: lst_len
  integer(i4b), allocatable :: lst(:)
  integer(i4b) :: result
  
  read(*,*) lst_len
  allocate(lst(lst_len))
  read(*,*) (lst(i), i=1, lst_len)
  
  result = solution(lst_len, lst)
  print *, result
  
contains

  function solution(lst_len, lst) result(res)
    implicit none
    integer(i4b), intent(in) :: lst_len
    integer(i4b), intent(in) :: lst(:)
    integer(i4b) :: res
    integer(i4b) :: i
    
    res = 0
    do i = 1, lst_len
      if (mod(i, 2) /= 0 .and. mod(lst(i), 2) /= 0) then
        res = res + lst(i)
      end if
    end do
  end function solution

end program test_solution
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,32 @@
-program sum_odd_at_even_positions
+program test_solution
+  implicit none
+  integer, parameter :: i4b = selected_int_kind(9)
+  integer(i4b) :: lst_len
+  integer(i4b), allocatable :: lst(:)
+  integer(i4b) :: result
+  
+  read(*,*) lst_len
+  allocate(lst(lst_len))
+  read(*,*) (lst(i), i=1, lst_len)
+  
+  result = solution(lst_len, lst)
+  print *, result
+  
+contains
+
+  function solution(lst_len, lst) result(res)
     implicit none
-    integer :: n
-    integer, allocatable :: lst(:)
-    integer :: i
-    integer :: sum = 0
+    integer(i4b), intent(in) :: lst_len
+    integer(i4b), intent(in) :: lst(:)
+    integer(i4b) :: res
+    integer(i4b) :: i
     
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
+    res = 0
+    do i = 1, lst_len
+      if (mod(i, 2) /= 0 .and. mod(lst(i), 2) /= 0) then
+        res = res + lst(i)
+      end if
     end do
-    
-    ! Output result
-    write (*, *) sum
-    
-    ! Deallocate
-    deallocate(lst)
-end program sum_odd_at_even_positions
+  end function solution
+
+end program test_solution
```
