# Failure case: ft_ABC_Strong_humaneval_mistral_conc3 / task 45

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_compile_err`


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
    "ft": 8
  },
  "num_nonempty_lines": {
    "base": 11,
    "ft": 8
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
  real :: a, h, area
  read(*,*) a
  read(*,*) h
  area = 0.5 * a * h
  print(*,*) area
end program triangle_area
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,14 +1,8 @@
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
+  real :: a, h, area
+  read(*,*) a
+  read(*,*) h
+  area = 0.5 * a * h
+  print(*,*) area
 end program triangle_area
```
