# Failure case: ft_ABC_filtered_manual_humaneval_mistral_conc20 / task 45

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that computes the area of a triangle given the base length and height.
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
    "base": 14,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 11,
    "ft": 0
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  },
  "uses_implicit_none": {
    "base": true,
    "ft": false
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
    real :: base, height, area
    
    ! Read base and height from input
    read *, base
    read *, height
    
    ! Calculate area of triangle
    area = 0.5 * base * height
    
    ! Output the result
    write (*, *) area
end program triangle_area
```


## FT generated code

```fortran

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,14 +0,0 @@
-program triangle_area
-    implicit none
-    real :: base, height, area
-    
-    ! Read base and height from input
-    read *, base
-    read *, height
-    
-    ! Calculate area of triangle
-    area = 0.5 * base * height
-    
-    ! Output the result
-    write (*, *) area
-end program triangle_area
```
