# Failure case: ft_B_humaneval_mistral_conc20 / task 157

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `status_ok`


## Prompt

```text
Write a Fortran90 program that determines if three given side lengths can form a right-angled triangle.
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
  "num_lines": {
    "base": 23,
    "ft": 13
  },
  "num_nonempty_lines": {
    "base": 19,
    "ft": 10
  }
}
```


## Base generated code

```fortran
program right_triangle_check
    implicit none
    integer :: a, b, c
    integer :: a_sq, b_sq, c_sq
    
    ! Read three side lengths from stdin
    read *, a
    read *, b
    read *, c
    
    ! Calculate squares of each side
    a_sq = a * a
    b_sq = b * b
    c_sq = c * c
    
    ! Check if any combination satisfies Pythagorean theorem
    if ((a_sq + b_sq == c_sq) .or. (a_sq + c_sq == b_sq) .or. (b_sq + c_sq == a_sq)) then
        print *, .true.
    else
        print *, .false.
    end if
    
end program right_triangle_check
```


## FT generated code

```fortran
program right_angle_triangle
  implicit none
  integer :: a, b, c
  logical :: result

  read *, a
  read *, b
  read *, c

  result = (a*a + b*b == c*c) .or. (a*a + c*c == b*b) .or. (b*b + c*c == a*a)

  print *, result
end program right_angle_triangle
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,23 +1,13 @@
-program right_triangle_check
-    implicit none
-    integer :: a, b, c
-    integer :: a_sq, b_sq, c_sq
-    
-    ! Read three side lengths from stdin
-    read *, a
-    read *, b
-    read *, c
-    
-    ! Calculate squares of each side
-    a_sq = a * a
-    b_sq = b * b
-    c_sq = c * c
-    
-    ! Check if any combination satisfies Pythagorean theorem
-    if ((a_sq + b_sq == c_sq) .or. (a_sq + c_sq == b_sq) .or. (b_sq + c_sq == a_sq)) then
-        print *, .true.
-    else
-        print *, .false.
-    end if
-    
-end program right_triangle_check
+program right_angle_triangle
+  implicit none
+  integer :: a, b, c
+  logical :: result
+
+  read *, a
+  read *, b
+  read *, c
+
+  result = (a*a + b*b == c*c) .or. (a*a + c*c == b*b) .or. (b*b + c*c == a*a)
+
+  print *, result
+end program right_angle_triangle
```
