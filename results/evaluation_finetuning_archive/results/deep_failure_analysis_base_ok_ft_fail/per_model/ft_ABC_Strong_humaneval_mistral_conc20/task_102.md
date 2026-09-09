# Failure case: ft_ABC_Strong_humaneval_mistral_conc20 / task 102

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


## Prompt

```text
Write a Fortran90 program that takes two positive integers x and y and returns the largest even integer within the range [x, y] inclusive. If there is no such even number, return -1.
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
    "base": 26,
    "ft": 43
  },
  "num_nonempty_lines": {
    "base": 21,
    "ft": 33
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
program choose_num
    implicit none
    integer :: x, y, result

    ! Read input from stdin
    read *, x
    read *, y

    ! Find the largest even number in range [x, y]
    if (y < x) then
        result = -1
    else if (mod(y, 2) == 0) then
        result = y
    else
        result = y - 1
    end if

    ! If result is less than x, no even number exists in range
    if (result < x) then
        result = -1
    end if

    ! Output the result to stdout
    write (*, *) result

end program choose_num
```


## FT generated code

```fortran
program choose_num_demo
  implicit none
  integer :: x, y, result

  ! Read input values
  read(*,*) x
  read(*,*) y

  ! Call the function
  result = choose_num(x, y)

  ! Output the result
  print(*,*) result

contains

  function choose_num(x, y) result(res)
    implicit none
    integer, intent(in) :: x, y
    integer :: res
    integer :: even_num

    if (x > y) then
      res = -1
      return
    end if

    ! Find the largest even number in [x, y]
    if (mod(y, 2) == 0) then
      even_num = y
    else
      even_num = y - 1
    end if

    if (even_num < x) then
      res = -1
    else
      res = even_num
    end if

  end function choose_num

end program choose_num_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,43 @@
-program choose_num
+program choose_num_demo
+  implicit none
+  integer :: x, y, result
+
+  ! Read input values
+  read(*,*) x
+  read(*,*) y
+
+  ! Call the function
+  result = choose_num(x, y)
+
+  ! Output the result
+  print(*,*) result
+
+contains
+
+  function choose_num(x, y) result(res)
     implicit none
-    integer :: x, y, result
+    integer, intent(in) :: x, y
+    integer :: res
+    integer :: even_num
 
-    ! Read input from stdin
-    read *, x
-    read *, y
-
-    ! Find the largest even number in range [x, y]
-    if (y < x) then
-        result = -1
-    else if (mod(y, 2) == 0) then
-        result = y
-    else
-        result = y - 1
+    if (x > y) then
+      res = -1
+      return
     end if
 
-    ! If result is less than x, no even number exists in range
-    if (result < x) then
-        result = -1
+    ! Find the largest even number in [x, y]
+    if (mod(y, 2) == 0) then
+      even_num = y
+    else
+      even_num = y - 1
     end if
 
-    ! Output the result to stdout
-    write (*, *) result
+    if (even_num < x) then
+      res = -1
+    else
+      res = even_num
+    end if
 
-end program choose_num
+  end function choose_num
+
+end program choose_num_demo
```
