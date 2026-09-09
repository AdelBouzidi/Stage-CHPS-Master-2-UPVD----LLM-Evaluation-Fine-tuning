# Failure case: ft_AB_shuffle_humaneval_mistral_conc15 / task 157

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
  "uses_hardcoded_arrays": {
    "base": false,
    "ft": true
  },
  "uses_hardcoded_scalars": {
    "base": false,
    "ft": true
  },
  "uses_read_stdin": {
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
program right_angle_triangle
  implicit none
  integer :: a, b, c
  logical :: result

  ! Read input values
  read(*,*) a
  read(*,*) b
  read(*,*) c

  ! Check if it's a right-angled triangle
  result = right_angle_triangle(a, b, c)

  ! Output result
  print *, result

contains

  logical function right_angle_triangle(a, b, c)
    integer, intent(in) :: a, b, c
    integer :: sides(3)
    integer :: i, j

    ! Store sides in array
    sides = [a, b, c]

    ! Sort the sides (simple bubble sort)
    do i = 1, 2
      do j = i+1, 3
        if (sides(j) < sides(i)) then
          sides(i) = sides(i) + sides(j)
          sides(j) = sides(i) - sides(j)
          sides(i) = sides(i) - sides(j)
        end if
      end do
    end do

    ! Check Pythagorean theorem: a^2 + b^2 = c^2
    if (sides(1)**2 + sides(2)**2 == sides(3)**2) then
      right_angle_triangle = .true.
    else
      right_angle_triangle = .false.
    end if
  end function right_angle_triangle

end program right_angle_triangle
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,23 +1,46 @@
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
+program right_angle_triangle
+  implicit none
+  integer :: a, b, c
+  logical :: result
+
+  ! Read input values
+  read(*,*) a
+  read(*,*) b
+  read(*,*) c
+
+  ! Check if it's a right-angled triangle
+  result = right_angle_triangle(a, b, c)
+
+  ! Output result
+  print *, result
+
+contains
+
+  logical function right_angle_triangle(a, b, c)
+    integer, intent(in) :: a, b, c
+    integer :: sides(3)
+    integer :: i, j
+
+    ! Store sides in array
+    sides = [a, b, c]
+
+    ! Sort the sides (simple bubble sort)
+    do i = 1, 2
+      do j = i+1, 3
+        if (sides(j) < sides(i)) then
+          sides(i) = sides(i) + sides(j)
+          sides(j) = sides(i) - sides(j)
+          sides(i) = sides(i) - sides(j)
+        end if
+      end do
+    end do
+
+    ! Check Pythagorean theorem: a^2 + b^2 = c^2
+    if (sides(1)**2 + sides(2)**2 == sides(3)**2) then
+      right_angle_triangle = .true.
     else
-        print *, .false.
+      right_angle_triangle = .false.
     end if
-    
-end program right_triangle_check
+  end function right_angle_triangle
+
+end program right_angle_triangle
```
