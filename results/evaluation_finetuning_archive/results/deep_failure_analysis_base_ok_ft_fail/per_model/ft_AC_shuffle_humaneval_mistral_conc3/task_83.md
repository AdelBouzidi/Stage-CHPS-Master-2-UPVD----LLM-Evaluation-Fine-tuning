# Failure case: ft_AC_shuffle_humaneval_mistral_conc3 / task 83

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


## Prompt

```text
Write a Fortran90 program that returns the count of n-digit positive integers that start or end with 1.
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
    "base": 16,
    "ft": 28
  },
  "num_nonempty_lines": {
    "base": 12,
    "ft": 22
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
program count_start_or_end_one
    implicit none
    integer :: n
    integer :: result

    read(*,*) n

    if (n == 1) then
        result = 1
    else
        result = 18 * 10**(n - 2)
    end if

    write(*,*) result

end program count_start_or_end_one
```


## FT generated code

```fortran
program starts_one_ends
    implicit none
    integer :: n
    integer :: result

    ! Read input from stdin
    read(*,*) n

    ! Calculate result
    result = starts_one_ends(n)

    ! Print result to stdout
    print *, result

contains

    function starts_one_ends(n) result(res)
        implicit none
        integer, intent(in) :: n
        integer :: res
        if (n == 1) then
            res = 1
        else
            res = 9 * 10**(n-1) + 10**(n-1) - 10**(n-2)
        end if
    end function starts_one_ends

end program starts_one_ends
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,16 +1,28 @@
-program count_start_or_end_one
+program starts_one_ends
     implicit none
     integer :: n
     integer :: result
 
+    ! Read input from stdin
     read(*,*) n
 
-    if (n == 1) then
-        result = 1
-    else
-        result = 18 * 10**(n - 2)
-    end if
+    ! Calculate result
+    result = starts_one_ends(n)
 
-    write(*,*) result
+    ! Print result to stdout
+    print *, result
 
-end program count_start_or_end_one
+contains
+
+    function starts_one_ends(n) result(res)
+        implicit none
+        integer, intent(in) :: n
+        integer :: res
+        if (n == 1) then
+            res = 1
+        else
+            res = 9 * 10**(n-1) + 10**(n-1) - 10**(n-2)
+        end if
+    end function starts_one_ends
+
+end program starts_one_ends
```
