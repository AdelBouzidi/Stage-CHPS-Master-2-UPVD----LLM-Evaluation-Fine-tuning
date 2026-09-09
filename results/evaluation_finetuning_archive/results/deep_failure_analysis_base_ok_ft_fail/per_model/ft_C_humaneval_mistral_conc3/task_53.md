# Failure case: ft_C_humaneval_mistral_conc3 / task 53

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_compile_err`


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
{
  "uses_print_star": {
    "base": true,
    "ft": false
  },
  "uses_read_stdin": {
    "base": false,
    "ft": true
  }
}
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

  read(*,*) x
  read(*,*) y
  result = x + y
  print(*,*) result
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
+  read(*,*) x
+  read(*,*) y
+  result = x + y
+  print(*,*) result
 end program add_numbers
```
