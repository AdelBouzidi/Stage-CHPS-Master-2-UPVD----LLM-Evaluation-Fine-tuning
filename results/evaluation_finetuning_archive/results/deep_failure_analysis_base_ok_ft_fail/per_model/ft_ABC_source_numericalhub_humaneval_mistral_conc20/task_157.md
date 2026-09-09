# Failure case: ft_ABC_source_numericalhub_humaneval_mistral_conc20 / task 157

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ok`


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
    "ft": 57
  },
  "num_nonempty_lines": {
    "base": 19,
    "ft": 48
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
program right_angle_triangle_test
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

  function right_angle_triangle(a, b, c) result(res)
    implicit none
    integer, intent(in) :: a, b, c
    logical :: res
    integer :: a2, b2, c2
    integer :: max_side, other1, other2

    ! Sort the sides to identify the largest
    if (a >= b) then
      if (a >= c) then
        max_side = a
        other1 = b
        other2 = c
      else
        max_side = c
        other1 = a
        other2 = b
      end if
    else
      if (b >= c) then
        max_side = b
        other1 = a
        other2 = c
      else
        max_side = c
        other1 = b
        other2 = a
      end if
    end if

    ! Check Pythagorean theorem
    a2 = other1**2
    b2 = other2**2
    c2 = max_side**2
    res = (a2 + b2 == c2)

  end function right_angle_triangle

end program right_angle_triangle_test
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,23 +1,57 @@
-program right_triangle_check
+program right_angle_triangle_test
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
+  function right_angle_triangle(a, b, c) result(res)
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
+    logical :: res
+    integer :: a2, b2, c2
+    integer :: max_side, other1, other2
+
+    ! Sort the sides to identify the largest
+    if (a >= b) then
+      if (a >= c) then
+        max_side = a
+        other1 = b
+        other2 = c
+      else
+        max_side = c
+        other1 = a
+        other2 = b
+      end if
     else
-        print *, .false.
+      if (b >= c) then
+        max_side = b
+        other1 = a
+        other2 = c
+      else
+        max_side = c
+        other1 = b
+        other2 = a
+      end if
     end if
-    
-end program right_triangle_check
+
+    ! Check Pythagorean theorem
+    a2 = other1**2
+    b2 = other2**2
+    c2 = max_side**2
+    res = (a2 + b2 == c2)
+
+  end function right_angle_triangle
+
+end program right_angle_triangle_test
```
