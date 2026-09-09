# Failure case: ft_A_half1_humaneval_mistral_conc20 / task 100

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_compile_err`


## Prompt

```text
Write a Fortran90 program that, given a positive integer n, creates a pile (array) of n levels of stones. The first level has n stones and each subsequent level has the next odd number if n is odd or the next even number if n is even.
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
  "num_lines": {
    "base": 20,
    "ft": 28
  },
  "num_nonempty_lines": {
    "base": 15,
    "ft": 22
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
  }
}
```


## Base generated code

```fortran
program stone_pile
    implicit none
    integer :: n, i
    integer, allocatable :: stones(:)
    
    read(*,*) n
    
    allocate(stones(n))
    stones(1) = n
    
    do i = 2, n
        stones(i) = stones(i-1) + 2
    end do
    
    do i = 1, n
        if (i > 1) write(*,*) ' '
        write(*,*) stones(i)
    end do
    
end program stone_pile
```


## FT generated code

```fortran
program main
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  call make_a_pile(n, result)
  
  ! Print output
  write(*,*) result
contains

  subroutine make_a_pile(n, result)
    implicit none
    integer, intent(in) :: n
    integer, intent(out) :: result(:)
    integer :: i
    
    allocate(result(n))
    do i = 1, n
      result(i) = n + 2*(i-1)
    end do
  end subroutine make_a_pile

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,20 +1,28 @@
-program stone_pile
+program main
+  implicit none
+  integer :: n
+  integer, allocatable :: result(:)
+  
+  ! Read input
+  read(*,*) n
+  
+  ! Call the function
+  call make_a_pile(n, result)
+  
+  ! Print output
+  write(*,*) result
+contains
+
+  subroutine make_a_pile(n, result)
     implicit none
-    integer :: n, i
-    integer, allocatable :: stones(:)
+    integer, intent(in) :: n
+    integer, intent(out) :: result(:)
+    integer :: i
     
-    read(*,*) n
-    
-    allocate(stones(n))
-    stones(1) = n
-    
-    do i = 2, n
-        stones(i) = stones(i-1) + 2
+    allocate(result(n))
+    do i = 1, n
+      result(i) = n + 2*(i-1)
     end do
-    
-    do i = 1, n
-        if (i > 1) write(*,*) ' '
-        write(*,*) stones(i)
-    end do
-    
-end program stone_pile
+  end subroutine make_a_pile
+
+end program main
```
