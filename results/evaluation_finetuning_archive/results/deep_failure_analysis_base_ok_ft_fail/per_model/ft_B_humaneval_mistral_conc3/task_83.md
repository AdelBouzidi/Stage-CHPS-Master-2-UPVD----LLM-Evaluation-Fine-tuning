# Failure case: ft_B_humaneval_mistral_conc3 / task 83

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


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
  "num_lines": {
    "base": 16,
    "ft": 15
  },
  "num_nonempty_lines": {
    "base": 12,
    "ft": 11
  },
  "uses_read_stdin": {
    "base": true,
    "ft": false
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
  integer :: n, result

  read *, n

  if (n == 1) then
    result = 1
  else
    result = 10**(n-1) + 8*10**(n-2)
  end if

  write *, result

end program starts_one_ends
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,16 +1,15 @@
-program count_start_or_end_one
-    implicit none
-    integer :: n
-    integer :: result
+program starts_one_ends
+  implicit none
+  integer :: n, result
 
-    read(*,*) n
+  read *, n
 
-    if (n == 1) then
-        result = 1
-    else
-        result = 18 * 10**(n - 2)
-    end if
+  if (n == 1) then
+    result = 1
+  else
+    result = 10**(n-1) + 8*10**(n-2)
+  end if
 
-    write(*,*) result
+  write *, result
 
-end program count_start_or_end_one
+end program starts_one_ends
```
