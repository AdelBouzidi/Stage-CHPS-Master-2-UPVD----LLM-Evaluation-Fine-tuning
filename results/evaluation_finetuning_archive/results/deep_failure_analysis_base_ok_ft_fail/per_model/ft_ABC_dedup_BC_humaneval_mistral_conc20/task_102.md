# Failure case: ft_ABC_dedup_BC_humaneval_mistral_conc20 / task 102

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `static_modifies_intent_in_possible, status_ok`


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
    "ft": 34
  },
  "num_nonempty_lines": {
    "base": 21,
    "ft": 26
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
program choose_num_demo
  implicit none
  integer :: x, y, result

  ! Read input
  read *, x
  read *, y

  ! Call the function
  result = choose_num(x, y)

  ! Output result
  print *, result

contains

  function choose_num(x, y) result(res)
    implicit none
    integer, intent(in) :: x, y
    integer :: res
    integer :: i

    ! Find the largest even number in range [x, y]
    do i = y, x, -1
      if (mod(i, 2) == 0) then
        res = i
        return
      end if
    end do

    res = -1
  end function choose_num

end program choose_num_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,34 @@
-program choose_num
+program choose_num_demo
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
+  ! Output result
+  print *, result
+
+contains
+
+  function choose_num(x, y) result(res)
     implicit none
-    integer :: x, y, result
-
-    ! Read input from stdin
-    read *, x
-    read *, y
+    integer, intent(in) :: x, y
+    integer :: res
+    integer :: i
 
     ! Find the largest even number in range [x, y]
-    if (y < x) then
-        result = -1
-    else if (mod(y, 2) == 0) then
-        result = y
-    else
-        result = y - 1
-    end if
+    do i = y, x, -1
+      if (mod(i, 2) == 0) then
+        res = i
+        return
+      end if
+    end do
 
-    ! If result is less than x, no even number exists in range
-    if (result < x) then
-        result = -1
-    end if
+    res = -1
+  end function choose_num
 
-    ! Output the result to stdout
-    write (*, *) result
-
-end program choose_num
+end program choose_num_demo
```
