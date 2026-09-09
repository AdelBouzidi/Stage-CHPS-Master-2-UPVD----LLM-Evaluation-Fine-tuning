# Failure case: ft_ABC_filtered_reject_humaneval_mistral_conc20 / task 102

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


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
    "ft": 35
  },
  "num_nonempty_lines": {
    "base": 21,
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

  ! Read input
  read *, x
  read *, y

  ! Call the function
  result = choose_num(x, y)

  ! Print output
  print *, result

contains

  function choose_num(x, y) result(res)
    implicit none
    integer, intent(in) :: x, y
    integer :: res

    if (x > y) then
      res = -1
    else
      res = y
      if (mod(res, 2) /= 0) then
        res = res - 1
      end if
      if (res < x) then
        res = -1
      end if
    end if
  end function choose_num

end program choose_num
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,35 @@
 program choose_num
+  implicit none
+  integer :: x, y, result
+
+  ! Read input
+  read *, x
+  read *, y
+
+  ! Call the function
+  result = choose_num(x, y)
+
+  ! Print output
+  print *, result
+
+contains
+
+  function choose_num(x, y) result(res)
     implicit none
-    integer :: x, y, result
+    integer, intent(in) :: x, y
+    integer :: res
 
-    ! Read input from stdin
-    read *, x
-    read *, y
-
-    ! Find the largest even number in range [x, y]
-    if (y < x) then
-        result = -1
-    else if (mod(y, 2) == 0) then
-        result = y
+    if (x > y) then
+      res = -1
     else
-        result = y - 1
+      res = y
+      if (mod(res, 2) /= 0) then
+        res = res - 1
+      end if
+      if (res < x) then
+        res = -1
+      end if
     end if
-
-    ! If result is less than x, no even number exists in range
-    if (result < x) then
-        result = -1
-    end if
-
-    ! Output the result to stdout
-    write (*, *) result
+  end function choose_num
 
 end program choose_num
```
