# Failure case: ft_AC_antineighbor_humaneval_mistral_conc20 / task 24

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
  "num_lines": {
    "base": 21,
    "ft": 20
  },
  "num_nonempty_lines": {
    "base": 18,
    "ft": 16
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
program largest_divisor
  implicit none
  integer :: n, result

  ! Read input
  read *, n

  ! Find largest divisor smaller than n
  result = 1
  do i = n/2, 1, -1
    if (mod(n, i) == 0) then
      result = i
      exit
    end if
  end do

  ! Output result
  print *, result

end program largest_divisor
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,21 +1,20 @@
 program largest_divisor
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
-        end do
+  implicit none
+  integer :: n, result
+
+  ! Read input
+  read *, n
+
+  ! Find largest divisor smaller than n
+  result = 1
+  do i = n/2, 1, -1
+    if (mod(n, i) == 0) then
+      result = i
+      exit
     end if
-    
-    ! Output result
-    write (*, *) result
+  end do
+
+  ! Output result
+  print *, result
+
 end program largest_divisor
```
