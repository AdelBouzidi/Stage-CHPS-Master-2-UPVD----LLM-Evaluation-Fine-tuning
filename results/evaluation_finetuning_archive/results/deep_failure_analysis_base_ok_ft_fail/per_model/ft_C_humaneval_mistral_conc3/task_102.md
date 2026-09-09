# Failure case: ft_C_humaneval_mistral_conc3 / task 102

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ineq`


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
    "ft": 20
  },
  "num_nonempty_lines": {
    "base": 21,
    "ft": 17
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
    read(*, *) x
    read(*, *) y

    ! Find the largest even number in range [x, y]
    if (y < x) then
        result = -1
    else if (mod(y, 2) == 0) then
        result = y
    else
        result = y - 1
    end if

    ! Output result
    print *, result
end program choose_num
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -2,9 +2,9 @@
     implicit none
     integer :: x, y, result
 
-    ! Read input from stdin
-    read *, x
-    read *, y
+    ! Read input
+    read(*, *) x
+    read(*, *) y
 
     ! Find the largest even number in range [x, y]
     if (y < x) then
@@ -15,12 +15,6 @@
         result = y - 1
     end if
 
-    ! If result is less than x, no even number exists in range
-    if (result < x) then
-        result = -1
-    end if
-
-    ! Output the result to stdout
-    write (*, *) result
-
+    ! Output result
+    print *, result
 end program choose_num
```
