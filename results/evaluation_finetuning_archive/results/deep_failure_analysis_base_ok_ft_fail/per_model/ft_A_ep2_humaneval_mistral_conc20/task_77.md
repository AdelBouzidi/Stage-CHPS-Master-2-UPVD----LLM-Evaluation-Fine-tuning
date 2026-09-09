# Failure case: ft_A_ep2_humaneval_mistral_conc20 / task 77

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_output_labels, static_stdin_read, status_compile_err`


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
  "has_labels_in_output": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 29,
    "ft": 14
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 11
  },
  "uses_hardcoded_scalars": {
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
  implicit none
  integer :: a
  logical :: result

  ! Read input from stdin
  read(*,*) a

  ! Call the iscube function
  result = iscube(a)

  ! Output the result
  print *, 'Output: ', result
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,29 +1,14 @@
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
+  implicit none
+  integer :: a
+  logical :: result
+
+  ! Read input from stdin
+  read(*,*) a
+
+  ! Call the iscube function
+  result = iscube(a)
+
+  ! Output the result
+  print *, 'Output: ', result
+end program main
```
