# Failure case: ft_B_humaneval_mistral_conc20 / task 45

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `status_ok`


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
  "num_lines": {
    "base": 14,
    "ft": 9
  },
  "num_nonempty_lines": {
    "base": 11,
    "ft": 8
  },
  "uses_print_star": {
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
program triangle_area
  implicit none
  real :: base, height, area

  read *, base
  read *, height
  area = 0.5 * base * height
  print *, area
end program triangle_area
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,14 +1,9 @@
 program triangle_area
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
+  implicit none
+  real :: base, height, area
+
+  read *, base
+  read *, height
+  area = 0.5 * base * height
+  print *, area
 end program triangle_area
```
