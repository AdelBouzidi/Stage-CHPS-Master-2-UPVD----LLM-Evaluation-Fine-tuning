# Failure case: ft_C_then_A_humaneval_mistral_conc3 / task 55

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_compile_err`


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
  "num_functions": {
    "base": 0,
    "ft": 2
  },
  "num_lines": {
    "base": 29,
    "ft": 18
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 18
  },
  "uses_print_star": {
    "base": false,
    "ft": true
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
  print *, result
contains
  integer function fib(n)
    integer, intent(in) :: n
    if (n <= 0) then
      fib = 0
    else if (n == 1) then
      fib = 1
    else
      fib = fib(n-1) + fib(n-2)
    end if
  end function fib
end program fib
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,29 +1,18 @@
-program fibonacci
-    implicit none
-    integer :: n, result
-    integer :: a, b, temp, i
-
-    ! Read input n
-    read *, n
-
-    ! Calculate Fibonacci number
+program fib
+  implicit none
+  integer :: n, result
+  read(*,*) n
+  result = fib(n)
+  print *, result
+contains
+  integer function fib(n)
+    integer, intent(in) :: n
     if (n <= 0) then
-        result = 0
+      fib = 0
     else if (n == 1) then
-        result = 1
-    else if (n == 2) then
-        result = 1
+      fib = 1
     else
-        a = 1
-        b = 1
-        do i = 3, n
-            temp = a + b
-            a = b
-            b = temp
-        end do
-        result = b
+      fib = fib(n-1) + fib(n-2)
     end if
-
-    ! Output result
-    write (*, *) result
-end program fibonacci
+  end function fib
+end program fib
```
