# Failure case: ft_B_then_A_humaneval_mistral_conc20 / task 100

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `static_modifies_intent_in_possible, status_ok`


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
  "modifies_intent_in_possible": {
    "base": false,
    "ft": true
  },
  "num_functions": {
    "base": 0,
    "ft": 2
  },
  "num_lines": {
    "base": 20,
    "ft": 25
  },
  "num_nonempty_lines": {
    "base": 15,
    "ft": 20
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
program pile_maker
      implicit none
      integer :: n
      integer, allocatable :: pile(:)

      read *, n
      pile = make_a_pile(n)
      print *, pile

    contains

      function make_a_pile(n) result(pile)
        implicit none
        integer, intent(in) :: n
        integer, allocatable :: pile(:)
        integer :: i

        allocate(pile(n))
        pile(1) = n
        do i = 2, n
          pile(i) = pile(i-1) + 2
        end do
      end function make_a_pile

    end program pile_maker
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,20 +1,25 @@
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
+program pile_maker
+      implicit none
+      integer :: n
+      integer, allocatable :: pile(:)
+
+      read *, n
+      pile = make_a_pile(n)
+      print *, pile
+
+    contains
+
+      function make_a_pile(n) result(pile)
+        implicit none
+        integer, intent(in) :: n
+        integer, allocatable :: pile(:)
+        integer :: i
+
+        allocate(pile(n))
+        pile(1) = n
+        do i = 2, n
+          pile(i) = pile(i-1) + 2
+        end do
+      end function make_a_pile
+
+    end program pile_maker
```
