# Failure case: ft_AC_antineighbor_humaneval_mistral_conc3 / task 77

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `status_ineq`

- Labels: `static_modifies_intent_in_possible, status_ineq`


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
    "ft": 35
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 28
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

  ! Print output
  print *, result

contains

  logical function iscube(a)
    implicit none
    integer, intent(in) :: a
    integer :: root
    real :: cube

    if (a == 0) then
       iscube = .true.
    else
       root = nint(abs(a)**(1.0/3.0))
       if (cube * root**3 == abs(a)) then
          iscube = .true.
       else
          iscube = .false.
       end if
    end if
  end function iscube

end program iscube_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,29 +1,35 @@
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
+  ! Print output
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
+    if (a == 0) then
+       iscube = .true.
     else
-        root = int((-a)**(1.0/3.0))
-        if ((-root)**3 == a) then
-            result = .true.
-        else
-            result = .false.
-        end if
+       root = nint(abs(a)**(1.0/3.0))
+       if (cube * root**3 == abs(a)) then
+          iscube = .true.
+       else
+          iscube = .false.
+       end if
     end if
-    
-    ! Output result
-    write (*, '(L)') result
-end program iscube
+  end function iscube
+
+end program iscube_demo
```
