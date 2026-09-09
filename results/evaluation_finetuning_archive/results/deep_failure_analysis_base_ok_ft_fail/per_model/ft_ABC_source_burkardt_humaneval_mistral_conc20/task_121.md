# Failure case: ft_ABC_source_burkardt_humaneval_mistral_conc20 / task 121

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
  "num_lines": {
    "base": 32,
    "ft": 36
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 29
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
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
program solution
  implicit none
  integer :: lst_len
  integer, allocatable :: lst(:)
  integer :: result

  read(*,*) lst_len
  allocate(lst(lst_len))
  read(*,*) lst

  result = 0
  do i = 1, lst_len
    if (mod(i - 1, 2) == 0 .and. mod(lst(i), 2) == 1) then
      result = result + lst(i)
    end if
  end do

  print *, result

contains

  subroutine solution(lst_len, lst, result)
    integer, intent(in) :: lst_len
    integer, intent(in) :: lst(lst_len)
    integer, intent(out) :: result
    integer :: i

    result = 0
    do i = 1, lst_len
      if (mod(i - 1, 2) == 0 .and. mod(lst(i), 2) == 1) then
        result = result + lst(i)
      end if
    end do
  end subroutine solution

end program solution
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,36 @@
-program sum_odd_at_even_positions
-    implicit none
-    integer :: n
-    integer, allocatable :: lst(:)
+program solution
+  implicit none
+  integer :: lst_len
+  integer, allocatable :: lst(:)
+  integer :: result
+
+  read(*,*) lst_len
+  allocate(lst(lst_len))
+  read(*,*) lst
+
+  result = 0
+  do i = 1, lst_len
+    if (mod(i - 1, 2) == 0 .and. mod(lst(i), 2) == 1) then
+      result = result + lst(i)
+    end if
+  end do
+
+  print *, result
+
+contains
+
+  subroutine solution(lst_len, lst, result)
+    integer, intent(in) :: lst_len
+    integer, intent(in) :: lst(lst_len)
+    integer, intent(out) :: result
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
+
+    result = 0
+    do i = 1, lst_len
+      if (mod(i - 1, 2) == 0 .and. mod(lst(i), 2) == 1) then
+        result = result + lst(i)
+      end if
     end do
-    
-    ! Output result
-    write (*, *) sum
-    
-    ! Deallocate
-    deallocate(lst)
-end program sum_odd_at_even_positions
+  end subroutine solution
+
+end program solution
```
