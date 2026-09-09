# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 24

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that for a given number n, finds the largest number that divides n evenly, smaller than n.
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
    "base": 21,
    "ft": 19
  },
  "num_nonempty_lines": {
    "base": 18,
    "ft": 19
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
program largest_divisor
    implicit none
    integer :: n, i, result
    
    ! Read input
    read *, n
    
    ! Find largest divisor smaller than n
    result = 1
    if (n > 1) then
        do i = n/2, 1, -1
            if (mod(n, i) == 0) then
                result = i
                exit
            end if
        end do
    end if
    
    ! Output result
    write (*, *) result
end program largest_divisor
```


## FT generated code

```fortran
program main
      implicit none
      integer :: n
      integer :: result
      n = 15
      result = largest_divisor(n)
      print *, result
    contains
      integer function largest_divisor(n)
        implicit none
        integer :: i
        result = n
        do i = 2, n/2
          if (mod(n, i) == 0) then
            result = i
          end if
        end do
      end function largest_divisor
    end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,21 +1,19 @@
-program largest_divisor
-    implicit none
-    integer :: n, i, result
-    
-    ! Read input
-    read *, n
-    
-    ! Find largest divisor smaller than n
-    result = 1
-    if (n > 1) then
-        do i = n/2, 1, -1
-            if (mod(n, i) == 0) then
-                result = i
-                exit
-            end if
+program main
+      implicit none
+      integer :: n
+      integer :: result
+      n = 15
+      result = largest_divisor(n)
+      print *, result
+    contains
+      integer function largest_divisor(n)
+        implicit none
+        integer :: i
+        result = n
+        do i = 2, n/2
+          if (mod(n, i) == 0) then
+            result = i
+          end if
         end do
-    end if
-    
-    ! Output result
-    write (*, *) result
-end program largest_divisor
+      end function largest_divisor
+    end program main
```
