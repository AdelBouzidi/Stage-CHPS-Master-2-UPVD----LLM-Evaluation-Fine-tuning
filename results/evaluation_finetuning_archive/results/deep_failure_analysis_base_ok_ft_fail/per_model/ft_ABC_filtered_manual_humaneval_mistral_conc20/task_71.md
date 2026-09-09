# Failure case: ft_ABC_filtered_manual_humaneval_mistral_conc20 / task 71

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that given the lengths of the three sides of a triangle, returns the area rounded to 2 decimal points if the triangle is valid, otherwise returns -1.
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
  "has_labels_in_output": {
    "base": true,
    "ft": false
  },
  "has_program": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 24,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 21,
    "ft": 0
  },
  "uses_implicit_none": {
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
program triangle_area
    implicit none
    real :: a, b, c, area, s
    real :: result

    ! Read input
    read *, a
    read *, b
    read *, c

    ! Check if triangle is valid using triangle inequality theorem
    if (a + b > c .and. a + c > b .and. b + c > a) then
        ! Calculate semi-perimeter
        s = (a + b + c) / 2.0
        ! Calculate area using Heron's formula
        area = sqrt(s * (s - a) * (s - b) * (s - c))
        ! Output area rounded to 2 decimal places
        write (*, '(F6.2)') area
    else
        ! Output -1 for invalid triangle
        write (*, '(I6)') -1
    end if

end program triangle_area
```


## FT generated code

```fortran

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,24 +0,0 @@
-program triangle_area
-    implicit none
-    real :: a, b, c, area, s
-    real :: result
-
-    ! Read input
-    read *, a
-    read *, b
-    read *, c
-
-    ! Check if triangle is valid using triangle inequality theorem
-    if (a + b > c .and. a + c > b .and. b + c > a) then
-        ! Calculate semi-perimeter
-        s = (a + b + c) / 2.0
-        ! Calculate area using Heron's formula
-        area = sqrt(s * (s - a) * (s - b) * (s - c))
-        ! Output area rounded to 2 decimal places
-        write (*, '(F6.2)') area
-    else
-        ! Output -1 for invalid triangle
-        write (*, '(I6)') -1
-    end if
-
-end program triangle_area
```
