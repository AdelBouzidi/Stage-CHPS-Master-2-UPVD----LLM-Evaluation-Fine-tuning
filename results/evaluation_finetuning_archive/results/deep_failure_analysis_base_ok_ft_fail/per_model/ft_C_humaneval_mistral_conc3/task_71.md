# Failure case: ft_C_humaneval_mistral_conc3 / task 71

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
  "has_labels_in_output": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 24,
    "ft": 23
  },
  "num_nonempty_lines": {
    "base": 21,
    "ft": 20
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

  ! Read the three sides
  read(*,*) a
  read(*,*) b
  read(*,*) c

  ! Check if triangle is valid (triangle inequality)
  if (a + b > c .and. a + c > b .and. b + c > a) then
    ! Calculate semi-perimeter
    s = (a + b + c) / 2.0
    ! Calculate area using Heron's formula
    area = sqrt(s * (s - a) * (s - b) * (s - c))
    ! Output rounded to 2 decimal places
    print*, trim(adjustl(format(f6.2, area)))
  else
    print*, -1.0
  end if

end program triangle_area
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,24 +1,23 @@
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
+  ! Read the three sides
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
+  if (a + b > c .and. a + c > b .and. b + c > a) then
+    ! Calculate semi-perimeter
+    s = (a + b + c) / 2.0
+    ! Calculate area using Heron's formula
+    area = sqrt(s * (s - a) * (s - b) * (s - c))
+    ! Output rounded to 2 decimal places
+    print*, trim(adjustl(format(f6.2, area)))
+  else
+    print*, -1.0
+  end if
 
 end program triangle_area
```
