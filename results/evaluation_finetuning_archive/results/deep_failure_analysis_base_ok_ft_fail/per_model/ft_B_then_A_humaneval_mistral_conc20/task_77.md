# Failure case: ft_B_then_A_humaneval_mistral_conc20 / task 77

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that takes an integer and returns true if it is the cube of some integer, and false otherwise.
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
    "base": 29,
    "ft": 9
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 9
  },
  "uses_module": {
    "base": false,
    "ft": true
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
program iscube
    implicit none
    integer :: a
    integer :: root
    logical :: result
    
    ! Read input
    read *, a
    
    ! Check if a is a perfect cube
    if (a >= 0) then
        root = int(a**(1.0/3.0))
        if (root**3 == a) then
            result = .true.
        else
            result = .false.
        end if
    else
        root = int((-a)**(1.0/3.0))
        if ((-root)**3 == a) then
            result = .true.
        else
            result = .false.
        end if
    end if
    
    ! Output result
    write (*, '(L)') result
end program iscube
```


## FT generated code

```fortran
program main
  use m
  implicit none
  integer :: a
  logical :: result
  a = 1
  result = iscube(a)
  print *, result
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,29 +1,9 @@
-program iscube
-    implicit none
-    integer :: a
-    integer :: root
-    logical :: result
-    
-    ! Read input
-    read *, a
-    
-    ! Check if a is a perfect cube
-    if (a >= 0) then
-        root = int(a**(1.0/3.0))
-        if (root**3 == a) then
-            result = .true.
-        else
-            result = .false.
-        end if
-    else
-        root = int((-a)**(1.0/3.0))
-        if ((-root)**3 == a) then
-            result = .true.
-        else
-            result = .false.
-        end if
-    end if
-    
-    ! Output result
-    write (*, '(L)') result
-end program iscube
+program main
+  use m
+  implicit none
+  integer :: a
+  logical :: result
+  a = 1
+  result = iscube(a)
+  print *, result
+end program main
```
