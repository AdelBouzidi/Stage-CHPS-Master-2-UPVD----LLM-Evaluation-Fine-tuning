# Failure case: ft_A_humaneval_mistral_conc20 / task 83

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_output_labels`

- Labels: `static_modifies_intent_in_possible, static_output_labels, status_ineq`


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
  "has_labels_in_output": {
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
    "ft": 26
  },
  "num_nonempty_lines": {
    "base": 12,
    "ft": 20
  },
  "uses_print_star": {
    "base": false,
    "ft": true
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
program starts_one_ends_demo
    implicit none
    integer :: n
    integer :: result

    ! Hardcoded input value
    n = 1

    ! Call the function
    result = starts_one_ends(n)

    ! Output the result
    print *, 'starts_one_ends(', n, ') =', result

contains

    integer function starts_one_ends(n)
        integer, intent(in) :: n
        if (n == 1) then
            starts_one_ends = 1
        else
            starts_one_ends = 10**(n-1) + 9*10**(n-2) - 10**(n-2)
        end if
    end function starts_one_ends

end program starts_one_ends_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,16 +1,26 @@
-program count_start_or_end_one
+program starts_one_ends_demo
     implicit none
     integer :: n
     integer :: result
 
-    read(*,*) n
+    ! Hardcoded input value
+    n = 1
 
-    if (n == 1) then
-        result = 1
-    else
-        result = 18 * 10**(n - 2)
-    end if
+    ! Call the function
+    result = starts_one_ends(n)
 
-    write(*,*) result
+    ! Output the result
+    print *, 'starts_one_ends(', n, ') =', result
 
-end program count_start_or_end_one
+contains
+
+    integer function starts_one_ends(n)
+        integer, intent(in) :: n
+        if (n == 1) then
+            starts_one_ends = 1
+        else
+            starts_one_ends = 10**(n-1) + 9*10**(n-2) - 10**(n-2)
+        end if
+    end function starts_one_ends
+
+end program starts_one_ends_demo
```
