# Failure case: ft_B_humaneval_mistral_conc20 / task 53

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `status_ok`


## Prompt

```text
Write a Fortran90 program that adds two numbers.
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
{}
```


## Base generated code

```fortran
program add_numbers
    implicit none
    integer :: x, y, result
    
    read *, x
    read *, y
    result = x + y
    print *, result
end program add_numbers
```


## FT generated code

```fortran
program add_numbers
  implicit none
  integer :: x, y, result
  
  read *, x
  read *, y
  result = x + y
  print *, result
end program add_numbers
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,9 +1,9 @@
 program add_numbers
-    implicit none
-    integer :: x, y, result
-    
-    read *, x
-    read *, y
-    result = x + y
-    print *, result
+  implicit none
+  integer :: x, y, result
+  
+  read *, x
+  read *, y
+  result = x + y
+  print *, result
 end program add_numbers
```
