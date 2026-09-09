# Failure case: ft_A_half1_humaneval_mistral_conc20 / task 157

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `status_ineq`

- Labels: `static_modifies_intent_in_possible, status_ineq`


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
  "has_debug_words": {
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
    "base": 23,
    "ft": 46
  },
  "num_nonempty_lines": {
    "base": 19,
    "ft": 37
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
program right_angle_triangle_demo
  implicit none
  integer :: a, b, c
  logical :: result

  ! Read input
  read *, a
  read *, b
  read *, c

  ! Determine if it's a right-angled triangle
  result = right_angle_triangle(a, b, c)

  ! Output result
  print *, result

contains

  logical function right_angle_triangle(a, b, c)
    implicit none
    integer, intent(in) :: a, b, c
    integer :: sides(3)
    integer :: i, max_idx

    ! Store sides in array
    sides(1) = a
    sides(2) = b
    sides(3) = c

    ! Find the maximum side
    max_idx = 1
    do i = 2, 3
      if (sides(i) > sides(max_idx)) then
        max_idx = i
      end if
    end do

    ! Check Pythagorean theorem
    if (sides(max_idx)**2 == sides((max_idx+2)/3)**2 + sides((max_idx+1)/3)**2) then
      right_angle_triangle = .true.
    else
      right_angle_triangle = .false.
    end if
  end function right_angle_triangle

end program right_angle_triangle_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,23 +1,46 @@
-program right_triangle_check
+program right_angle_triangle_demo
+  implicit none
+  integer :: a, b, c
+  logical :: result
+
+  ! Read input
+  read *, a
+  read *, b
+  read *, c
+
+  ! Determine if it's a right-angled triangle
+  result = right_angle_triangle(a, b, c)
+
+  ! Output result
+  print *, result
+
+contains
+
+  logical function right_angle_triangle(a, b, c)
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
+    integer, intent(in) :: a, b, c
+    integer :: sides(3)
+    integer :: i, max_idx
+
+    ! Store sides in array
+    sides(1) = a
+    sides(2) = b
+    sides(3) = c
+
+    ! Find the maximum side
+    max_idx = 1
+    do i = 2, 3
+      if (sides(i) > sides(max_idx)) then
+        max_idx = i
+      end if
+    end do
+
+    ! Check Pythagorean theorem
+    if (sides(max_idx)**2 == sides((max_idx+2)/3)**2 + sides((max_idx+1)/3)**2) then
+      right_angle_triangle = .true.
     else
-        print *, .false.
+      right_angle_triangle = .false.
     end if
-    
-end program right_triangle_check
+  end function right_angle_triangle
+
+end program right_angle_triangle_demo
```
