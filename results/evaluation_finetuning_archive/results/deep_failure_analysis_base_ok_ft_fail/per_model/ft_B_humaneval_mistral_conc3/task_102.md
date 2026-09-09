# Failure case: ft_B_humaneval_mistral_conc3 / task 102

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


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
  "num_lines": {
    "base": 26,
    "ft": 18
  },
  "num_nonempty_lines": {
    "base": 21,
    "ft": 14
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
program choose_num
  implicit none
  integer :: x, y, result

  read *, x
  read *, y

  if (x > y) then
    result = -1
  else if (mod(y, 2) == 0) then
    result = y
  else
    result = y - 1
  end if

  write *, result

end program choose_num
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,18 @@
 program choose_num
-    implicit none
-    integer :: x, y, result
+  implicit none
+  integer :: x, y, result
 
-    ! Read input from stdin
-    read *, x
-    read *, y
+  read *, x
+  read *, y
 
-    ! Find the largest even number in range [x, y]
-    if (y < x) then
-        result = -1
-    else if (mod(y, 2) == 0) then
-        result = y
-    else
-        result = y - 1
-    end if
+  if (x > y) then
+    result = -1
+  else if (mod(y, 2) == 0) then
+    result = y
+  else
+    result = y - 1
+  end if
 
-    ! If result is less than x, no even number exists in range
-    if (result < x) then
-        result = -1
-    end if
-
-    ! Output the result to stdout
-    write (*, *) result
+  write *, result
 
 end program choose_num
```
