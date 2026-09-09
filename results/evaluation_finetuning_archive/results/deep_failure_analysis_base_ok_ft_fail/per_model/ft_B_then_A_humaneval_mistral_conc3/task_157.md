# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 157

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


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
  "has_contains": {
    "base": false,
    "ft": true
  },
  "num_functions": {
    "base": 0,
    "ft": 2
  },
  "num_lines": {
    "base": 23,
    "ft": 21
  },
  "num_nonempty_lines": {
    "base": 19,
    "ft": 17
  },
  "uses_hardcoded_scalars": {
    "base": false,
    "ft": true
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
program right_angle_triangle_prog
  implicit none
  integer :: a, b, c
  logical :: res

  read *, a, b, c
  res = right_angle_triangle ( a, b, c )
  print *, res

contains

  logical function right_angle_triangle ( integer a, integer b, integer c )
    implicit none
    if ( a*a + b*b == c*c .or. a*a + c*c == b*b .or. b*b + c*c == a*a ) then
       right_angle_triangle = .true.
    else
       right_angle_triangle = .false.
    end if
  end function right_angle_triangle

end program right_angle_triangle_prog
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,23 +1,21 @@
-program right_triangle_check
+program right_angle_triangle_prog
+  implicit none
+  integer :: a, b, c
+  logical :: res
+
+  read *, a, b, c
+  res = right_angle_triangle ( a, b, c )
+  print *, res
+
+contains
+
+  logical function right_angle_triangle ( integer a, integer b, integer c )
     implicit none
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
+    if ( a*a + b*b == c*c .or. a*a + c*c == b*b .or. b*b + c*c == a*a ) then
+       right_angle_triangle = .true.
     else
-        print *, .false.
+       right_angle_triangle = .false.
     end if
-    
-end program right_triangle_check
+  end function right_angle_triangle
+
+end program right_angle_triangle_prog
```
