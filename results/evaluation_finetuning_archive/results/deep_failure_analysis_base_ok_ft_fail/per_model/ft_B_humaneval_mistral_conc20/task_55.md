# Failure case: ft_B_humaneval_mistral_conc20 / task 55

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `status_ok`


## Prompt

```text
Write a Fortran90 program that returns the n-th Fibonacci number.
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
  "has_debug_words": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 29,
    "ft": 24
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 21
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
program fibonacci
    implicit none
    integer :: n, result
    integer :: a, b, temp, i

    ! Read input n
    read *, n

    ! Calculate Fibonacci number
    if (n <= 0) then
        result = 0
    else if (n == 1) then
        result = 1
    else if (n == 2) then
        result = 1
    else
        a = 1
        b = 1
        do i = 3, n
            temp = a + b
            a = b
            b = temp
        end do
        result = b
    end if

    ! Output result
    write (*, *) result
end program fibonacci
```


## FT generated code

```fortran
program fibonacci
  implicit none
  integer :: n, a, b, temp, i

  ! Read input
  read *, n

  ! Calculate Fibonacci
  if (n <= 0) then
    print *, 0
  else if (n == 1) then
    print *, 1
  else
    a = 0
    b = 1
    do i = 2, n
      temp = a + b
      a = b
      b = temp
    end do
    print *, b
  end if

end program fibonacci
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,29 +1,24 @@
 program fibonacci
-    implicit none
-    integer :: n, result
-    integer :: a, b, temp, i
+  implicit none
+  integer :: n, a, b, temp, i
 
-    ! Read input n
-    read *, n
+  ! Read input
+  read *, n
 
-    ! Calculate Fibonacci number
-    if (n <= 0) then
-        result = 0
-    else if (n == 1) then
-        result = 1
-    else if (n == 2) then
-        result = 1
-    else
-        a = 1
-        b = 1
-        do i = 3, n
-            temp = a + b
-            a = b
-            b = temp
-        end do
-        result = b
-    end if
+  ! Calculate Fibonacci
+  if (n <= 0) then
+    print *, 0
+  else if (n == 1) then
+    print *, 1
+  else
+    a = 0
+    b = 1
+    do i = 2, n
+      temp = a + b
+      a = b
+      b = temp
+    end do
+    print *, b
+  end if
 
-    ! Output result
-    write (*, *) result
 end program fibonacci
```
