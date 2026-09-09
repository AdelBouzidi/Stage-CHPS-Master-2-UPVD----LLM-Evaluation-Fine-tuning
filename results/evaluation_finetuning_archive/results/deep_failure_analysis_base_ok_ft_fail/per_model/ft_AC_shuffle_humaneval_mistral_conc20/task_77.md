# Failure case: ft_AC_shuffle_humaneval_mistral_conc20 / task 77

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `static_modifies_intent_in_possible, status_ok`


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
    "base": 29,
    "ft": 41
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 31
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
program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Read input
  read *, a

  ! Call function
  result = iscube(a)

  ! Output result
  print *, result

contains

  logical function iscube(a)
    implicit none
    integer, intent(in) :: a
    integer :: root
    real :: cube

    if (a < 0) then
       root = -1
    else
       root = 0
    end if

    do while (root**3 < a)
       root = root + 1
    end do

    if (root**3 == a) then
       iscube = .true.
    else
       iscube = .false.
    end if

  end function iscube

end program iscube_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,29 +1,41 @@
-program iscube
+program iscube_demo
+  implicit none
+  integer :: a
+  logical :: result
+
+  ! Read input
+  read *, a
+
+  ! Call function
+  result = iscube(a)
+
+  ! Output result
+  print *, result
+
+contains
+
+  logical function iscube(a)
     implicit none
-    integer :: a
+    integer, intent(in) :: a
     integer :: root
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
+    real :: cube
+
+    if (a < 0) then
+       root = -1
     else
-        root = int((-a)**(1.0/3.0))
-        if ((-root)**3 == a) then
-            result = .true.
-        else
-            result = .false.
-        end if
+       root = 0
     end if
-    
-    ! Output result
-    write (*, '(L)') result
-end program iscube
+
+    do while (root**3 < a)
+       root = root + 1
+    end do
+
+    if (root**3 == a) then
+       iscube = .true.
+    else
+       iscube = .false.
+    end if
+
+  end function iscube
+
+end program iscube_demo
```
