# Failure case: ft_ABC_filtered_manual_humaneval_mistral_conc20 / task 157

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
  "has_program": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 23,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 19,
    "ft": 0
  },
  "uses_implicit_none": {
    "base": true,
    "ft": false
  },
  "uses_print_star": {
    "base": true,
    "ft": false
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

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,23 +0,0 @@
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
```
