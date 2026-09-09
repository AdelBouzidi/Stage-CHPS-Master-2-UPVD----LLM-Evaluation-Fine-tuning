# Failure case: ft_ABC_source_numericalhub_humaneval_mistral_conc20 / task 71

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ok`


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
  "has_contains": {
    "base": false,
    "ft": true
  },
  "has_debug_words": {
    "base": false,
    "ft": true
  },
  "has_labels_in_output": {
    "base": true,
    "ft": false
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
    "base": 24,
    "ft": 29
  },
  "num_nonempty_lines": {
    "base": 21,
    "ft": 24
  },
  "uses_hardcoded_scalars": {
    "base": false,
    "ft": true
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
  integer, parameter :: sp = kind(1.0)
  real(sp) :: a, b, c, area

  read(*,*) a
  read(*,*) b
  read(*,*) c
  area = triangle_area(a, b, c)
  print *, area

contains

  function triangle_area(a, b, c) result(area)
    implicit none
    real(sp), intent(in) :: a, b, c
    real(sp) :: area
    real(sp) :: s
    
    if (a <= 0.0_sp .or. b <= 0.0_sp .or. c <= 0.0_sp .or. &
        a + b <= c .or. a + c <= b .or. b + c <= a) then
      area = -1.0_sp
    else
      s = (a + b + c) / 2.0_sp
      area = sqrt(s * (s - a) * (s - b) * (s - c))
    end if
  end function triangle_area

end program triangle_area_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,24 +1,29 @@
-program triangle_area
+program triangle_area_demo
+  implicit none
+  integer, parameter :: sp = kind(1.0)
+  real(sp) :: a, b, c, area
+
+  read(*,*) a
+  read(*,*) b
+  read(*,*) c
+  area = triangle_area(a, b, c)
+  print *, area
+
+contains
+
+  function triangle_area(a, b, c) result(area)
     implicit none
-    real :: a, b, c, area, s
-    real :: result
+    real(sp), intent(in) :: a, b, c
+    real(sp) :: area
+    real(sp) :: s
+    
+    if (a <= 0.0_sp .or. b <= 0.0_sp .or. c <= 0.0_sp .or. &
+        a + b <= c .or. a + c <= b .or. b + c <= a) then
+      area = -1.0_sp
+    else
+      s = (a + b + c) / 2.0_sp
+      area = sqrt(s * (s - a) * (s - b) * (s - c))
+    end if
+  end function triangle_area
 
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
+end program triangle_area_demo
```
