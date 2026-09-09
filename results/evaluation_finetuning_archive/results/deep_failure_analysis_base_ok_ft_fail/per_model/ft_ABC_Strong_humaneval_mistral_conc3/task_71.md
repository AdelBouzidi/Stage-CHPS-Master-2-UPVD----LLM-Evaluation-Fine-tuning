# Failure case: ft_ABC_Strong_humaneval_mistral_conc3 / task 71

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_compile_err`


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
  "has_debug_words": {
    "base": false,
    "ft": true
  },
  "has_labels_in_output": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 24,
    "ft": 25
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
program triangle_area_demo
  implicit none
  real :: a, b, c, area
  logical :: valid

  ! Read input values
  read(*,*) a
  read(*,*) b
  read(*,*) c

  ! Check if triangle is valid (triangle inequality)
  valid = (a + b > c) .and. (a + c > b) .and. (b + c > a)

  if (valid) then
    ! Calculate semi-perimeter
    real :: s
    s = (a + b + c) / 2.0
    ! Calculate area using Heron's formula
    area = sqrt(s * (s - a) * (s - b) * (s - c))
    print *, area
  else
    print *, -1.0
  end if

end program triangle_area_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,24 +1,25 @@
-program triangle_area
-    implicit none
-    real :: a, b, c, area, s
-    real :: result
+program triangle_area_demo
+  implicit none
+  real :: a, b, c, area
+  logical :: valid
 
-    ! Read input
-    read *, a
-    read *, b
-    read *, c
+  ! Read input values
+  read(*,*) a
+  read(*,*) b
+  read(*,*) c
 
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
+  ! Check if triangle is valid (triangle inequality)
+  valid = (a + b > c) .and. (a + c > b) .and. (b + c > a)
 
-end program triangle_area
+  if (valid) then
+    ! Calculate semi-perimeter
+    real :: s
+    s = (a + b + c) / 2.0
+    ! Calculate area using Heron's formula
+    area = sqrt(s * (s - a) * (s - b) * (s - c))
+    print *, area
+  else
+    print *, -1.0
+  end if
+
+end program triangle_area_demo
```
