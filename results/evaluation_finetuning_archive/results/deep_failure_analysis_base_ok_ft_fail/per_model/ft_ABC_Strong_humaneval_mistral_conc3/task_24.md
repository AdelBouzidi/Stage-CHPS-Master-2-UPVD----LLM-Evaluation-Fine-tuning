# Failure case: ft_ABC_Strong_humaneval_mistral_conc3 / task 24

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ineq`


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
  "num_nonempty_lines": {
    "base": 18,
    "ft": 17
  },
  "uses_read_stdin": {
    "base": false,
    "ft": true
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

  ! Read input from stdin
  read(*,*) n

  ! Find the largest divisor of n (smaller than n)
  result = 1
  do while (result * 2 <= n)
    if (mod(n, result * 2) == 0) then
      result = result * 2
    else
      result = result + 1
    end if
  end do

  ! Output result to stdout
  write(*,*) result

end program largest_divisor
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,21 +1,21 @@
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
+  ! Read input from stdin
+  read(*,*) n
+
+  ! Find the largest divisor of n (smaller than n)
+  result = 1
+  do while (result * 2 <= n)
+    if (mod(n, result * 2) == 0) then
+      result = result * 2
+    else
+      result = result + 1
     end if
-    
-    ! Output result
-    write (*, *) result
+  end do
+
+  ! Output result to stdout
+  write(*,*) result
+
 end program largest_divisor
```
