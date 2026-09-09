# Failure case: ft_ABC_source_numerical_methods_humaneval_mistral_conc20 / task 77

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ok`


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
    "ft": 28
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 25
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
program iscube
    implicit none
    integer :: a
    integer :: root
    integer :: n
    logical :: result
    
    read(*,*) a
    
    if (a < 0) then
        n = -a
        root = int(n**(1.0/3.0))
        if (root**3 == n) then
            result = .true.
        else
            result = .false.
        end if
    else
        root = int(a**(1.0/3.0))
        if (root**3 == a) then
            result = .true.
        else
            result = .false.
        end if
    end if
    
    print *, result
end program iscube
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -2,28 +2,27 @@
     implicit none
     integer :: a
     integer :: root
+    integer :: n
     logical :: result
     
-    ! Read input
-    read *, a
+    read(*,*) a
     
-    ! Check if a is a perfect cube
-    if (a >= 0) then
+    if (a < 0) then
+        n = -a
+        root = int(n**(1.0/3.0))
+        if (root**3 == n) then
+            result = .true.
+        else
+            result = .false.
+        end if
+    else
         root = int(a**(1.0/3.0))
         if (root**3 == a) then
             result = .true.
         else
             result = .false.
         end if
-    else
-        root = int((-a)**(1.0/3.0))
-        if ((-root)**3 == a) then
-            result = .true.
-        else
-            result = .false.
-        end if
     end if
     
-    ! Output result
-    write (*, '(L)') result
+    print *, result
 end program iscube
```
