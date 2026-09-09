# Failure case: ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 100

- Base status: `ok`

- FT status: `runtime_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_runtime_err`


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
  "has_debug_words": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 20,
    "ft": 29
  },
  "num_nonempty_lines": {
    "base": 15,
    "ft": 22
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
  },
  "uses_allocate": {
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
program make_a_pile_demo
  implicit none
  integer :: n
  integer, allocatable :: pile(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  call make_a_pile(n, pile)
  
  ! Output the result
  print *, pile
  
contains

  subroutine make_a_pile(n, pile)
    implicit none
    integer, intent(in) :: n
    integer, intent(out) :: pile(n)
    integer :: i
    
    pile(1) = n
    do i = 2, n
      pile(i) = pile(i-1) + 2
    end do
  end subroutine make_a_pile

end program make_a_pile_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,20 +1,29 @@
-program stone_pile
+program make_a_pile_demo
+  implicit none
+  integer :: n
+  integer, allocatable :: pile(:)
+  
+  ! Read input
+  read(*,*) n
+  
+  ! Call the function
+  call make_a_pile(n, pile)
+  
+  ! Output the result
+  print *, pile
+  
+contains
+
+  subroutine make_a_pile(n, pile)
     implicit none
-    integer :: n, i
-    integer, allocatable :: stones(:)
+    integer, intent(in) :: n
+    integer, intent(out) :: pile(n)
+    integer :: i
     
-    read(*,*) n
-    
-    allocate(stones(n))
-    stones(1) = n
-    
+    pile(1) = n
     do i = 2, n
-        stones(i) = stones(i-1) + 2
+      pile(i) = pile(i-1) + 2
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
+end program make_a_pile_demo
```
