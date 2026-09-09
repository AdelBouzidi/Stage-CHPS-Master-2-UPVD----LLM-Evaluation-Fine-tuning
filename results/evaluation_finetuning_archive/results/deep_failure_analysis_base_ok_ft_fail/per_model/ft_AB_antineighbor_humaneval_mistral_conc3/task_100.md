# Failure case: ft_AB_antineighbor_humaneval_mistral_conc3 / task 100

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, status_compile_err`


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
  "num_lines": {
    "base": 20,
    "ft": 19
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
  integer, allocatable :: pile(:)
  
  ! Read input
  read *, n
  
  ! Create the pile
  allocate(pile(n))
  pile(1) = n
  do i = 2, n
    pile(i) = pile(i-1) + 2
  end do
  
  ! Output the result
  print *, pile
  
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,20 +1,19 @@
-program stone_pile
-    implicit none
-    integer :: n, i
-    integer, allocatable :: stones(:)
-    
-    read(*,*) n
-    
-    allocate(stones(n))
-    stones(1) = n
-    
-    do i = 2, n
-        stones(i) = stones(i-1) + 2
-    end do
-    
-    do i = 1, n
-        if (i > 1) write(*,*) ' '
-        write(*,*) stones(i)
-    end do
-    
-end program stone_pile
+program main
+  implicit none
+  integer :: n
+  integer, allocatable :: pile(:)
+  
+  ! Read input
+  read *, n
+  
+  ! Create the pile
+  allocate(pile(n))
+  pile(1) = n
+  do i = 2, n
+    pile(i) = pile(i-1) + 2
+  end do
+  
+  ! Output the result
+  print *, pile
+  
+end program main
```
