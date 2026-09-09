# Failure case: ft_A_ep2_humaneval_mistral_conc20 / task 83

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ineq`


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
    "ft": 21
  },
  "num_nonempty_lines": {
    "base": 12,
    "ft": 17
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

  ! Compute result
  if (n <= 0) then
    result = 0
  else if (n == 1) then
    result = 1
  else
    result = 2 * 10**(n-1) - 10**(n-2)
  end if

  ! Output result
  print *, result

end program starts_one_ends
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,16 +1,21 @@
-program count_start_or_end_one
-    implicit none
-    integer :: n
-    integer :: result
+program starts_one_ends
+  implicit none
+  integer :: n
+  integer :: result
 
-    read(*,*) n
+  ! Read input from stdin
+  read(*,*) n
 
-    if (n == 1) then
-        result = 1
-    else
-        result = 18 * 10**(n - 2)
-    end if
+  ! Compute result
+  if (n <= 0) then
+    result = 0
+  else if (n == 1) then
+    result = 1
+  else
+    result = 2 * 10**(n-1) - 10**(n-2)
+  end if
 
-    write(*,*) result
+  ! Output result
+  print *, result
 
-end program count_start_or_end_one
+end program starts_one_ends
```
