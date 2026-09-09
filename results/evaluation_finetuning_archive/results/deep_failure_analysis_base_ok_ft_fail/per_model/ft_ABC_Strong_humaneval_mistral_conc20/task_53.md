# Failure case: ft_ABC_Strong_humaneval_mistral_conc20 / task 53

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
    "base": 9,
    "ft": 21
  },
  "num_nonempty_lines": {
    "base": 8,
    "ft": 15
  },
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
program add_demo
  implicit none
  integer :: x, y, result

  ! Read input values
  read(*,*) x, y

  ! Calculate result
  result = add(x, y)

  ! Output result
  print(*,*) result

contains

  integer function add(x, y)
    integer, intent(in) :: x, y
    add = x + y
  end function add

end program add_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,9 +1,21 @@
-program add_numbers
-    implicit none
-    integer :: x, y, result
-    
-    read *, x
-    read *, y
-    result = x + y
-    print *, result
-end program add_numbers
+program add_demo
+  implicit none
+  integer :: x, y, result
+
+  ! Read input values
+  read(*,*) x, y
+
+  ! Calculate result
+  result = add(x, y)
+
+  ! Output result
+  print(*,*) result
+
+contains
+
+  integer function add(x, y)
+    integer, intent(in) :: x, y
+    add = x + y
+  end function add
+
+end program add_demo
```
