# Failure case: ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 83

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ineq`


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
    "ft": 34
  },
  "num_nonempty_lines": {
    "base": 12,
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
program starts_one_ends_demo
  implicit none
  integer :: n
  integer :: result

  ! Read input
  read(*,*) n

  ! Calculate result
  result = starts_one_ends(n)

  ! Output result
  print *, result

contains

  function starts_one_ends(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: i

    if (n == 1) then
      res = 1
    else
      res = 0
      do i = 1, n
        res = res * 10 + 1
      end do
    end if

  end function starts_one_ends

end program starts_one_ends_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,16 +1,34 @@
-program count_start_or_end_one
+program starts_one_ends_demo
+  implicit none
+  integer :: n
+  integer :: result
+
+  ! Read input
+  read(*,*) n
+
+  ! Calculate result
+  result = starts_one_ends(n)
+
+  ! Output result
+  print *, result
+
+contains
+
+  function starts_one_ends(n) result(res)
     implicit none
-    integer :: n
-    integer :: result
-
-    read(*,*) n
+    integer, intent(in) :: n
+    integer :: res
+    integer :: i
 
     if (n == 1) then
-        result = 1
+      res = 1
     else
-        result = 18 * 10**(n - 2)
+      res = 0
+      do i = 1, n
+        res = res * 10 + 1
+      end do
     end if
 
-    write(*,*) result
+  end function starts_one_ends
 
-end program count_start_or_end_one
+end program starts_one_ends_demo
```
