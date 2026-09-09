# Failure case: ft_AC_antineighbor_humaneval_mistral_conc20 / task 71

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ok`


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
  "num_lines": {
    "base": 24,
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
program triangle_area
  implicit none
  real :: a, b, c, area
  real :: s

  ! Read input values
  read(*,*) a
  read(*,*) b
  read(*,*) c

  ! Check if triangle is valid
  if (a + b > c .and. a + c > b .and. b + c > a) then
    s = (a + b + c) / 2.0
    area = sqrt(s * (s - a) * (s - b) * (s - c))
    print '(F6.2)', area
  else
    print *, -1.0
  end if

end program triangle_area
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,24 +1,20 @@
 program triangle_area
-    implicit none
-    real :: a, b, c, area, s
-    real :: result
+  implicit none
+  real :: a, b, c, area
+  real :: s
 
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
+  ! Check if triangle is valid
+  if (a + b > c .and. a + c > b .and. b + c > a) then
+    s = (a + b + c) / 2.0
+    area = sqrt(s * (s - a) * (s - b) * (s - c))
+    print '(F6.2)', area
+  else
+    print *, -1.0
+  end if
 
 end program triangle_area
```
