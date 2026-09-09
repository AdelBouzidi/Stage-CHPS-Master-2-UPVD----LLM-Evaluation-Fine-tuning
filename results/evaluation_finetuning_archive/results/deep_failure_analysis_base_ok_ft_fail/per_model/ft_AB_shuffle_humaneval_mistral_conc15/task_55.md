# Failure case: ft_AB_shuffle_humaneval_mistral_conc15 / task 55

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
  "has_contains": {
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
    "base": 29,
    "ft": 22
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 18
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  },
  "uses_read_stdin": {
    "base": false,
    "ft": true
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
program fib
  implicit none
  integer :: n, result

  read(*,*) n
  result = fib(n)
  write(*,*) result

contains

  recursive function fib(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    if (n <= 1) then
      res = n
    else
      res = fib(n-1) + fib(n-2)
    end if
  end function fib

end program fib
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,29 +1,22 @@
-program fibonacci
+program fib
+  implicit none
+  integer :: n, result
+
+  read(*,*) n
+  result = fib(n)
+  write(*,*) result
+
+contains
+
+  recursive function fib(n) result(res)
     implicit none
-    integer :: n, result
-    integer :: a, b, temp, i
+    integer, intent(in) :: n
+    integer :: res
+    if (n <= 1) then
+      res = n
+    else
+      res = fib(n-1) + fib(n-2)
+    end if
+  end function fib
 
-    ! Read input n
-    read *, n
-
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
-
-    ! Output result
-    write (*, *) result
-end program fibonacci
+end program fib
```
