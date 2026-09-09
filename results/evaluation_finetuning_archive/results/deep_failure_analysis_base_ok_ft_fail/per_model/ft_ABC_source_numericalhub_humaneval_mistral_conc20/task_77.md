# Failure case: ft_ABC_source_numericalhub_humaneval_mistral_conc20 / task 77

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ok`


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
    "ft": 32
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
program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Read input
  read(*,*) a

  ! Check if a is a perfect cube
  result = iscube(a)

  ! Output result
  print *, result

contains

  function iscube(a) result(res)
    implicit none
    integer, intent(in) :: a
    logical :: res
    integer :: n
    res = .false.
    if (a >= 0) then
      n = int(a**(1.0/3.0))
      if (n**3 == a) res = .true.
    else
      n = -int((-a)**(1.0/3.0))
      if (n**3 == a) res = .true.
    end if
  end function iscube

end program iscube_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,29 +1,32 @@
-program iscube
+program iscube_demo
+  implicit none
+  integer :: a
+  logical :: result
+
+  ! Read input
+  read(*,*) a
+
+  ! Check if a is a perfect cube
+  result = iscube(a)
+
+  ! Output result
+  print *, result
+
+contains
+
+  function iscube(a) result(res)
     implicit none
-    integer :: a
-    integer :: root
-    logical :: result
-    
-    ! Read input
-    read *, a
-    
-    ! Check if a is a perfect cube
+    integer, intent(in) :: a
+    logical :: res
+    integer :: n
+    res = .false.
     if (a >= 0) then
-        root = int(a**(1.0/3.0))
-        if (root**3 == a) then
-            result = .true.
-        else
-            result = .false.
-        end if
+      n = int(a**(1.0/3.0))
+      if (n**3 == a) res = .true.
     else
-        root = int((-a)**(1.0/3.0))
-        if ((-root)**3 == a) then
-            result = .true.
-        else
-            result = .false.
-        end if
+      n = -int((-a)**(1.0/3.0))
+      if (n**3 == a) res = .true.
     end if
-    
-    ! Output result
-    write (*, '(L)') result
-end program iscube
+  end function iscube
+
+end program iscube_demo
```
