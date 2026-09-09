# Failure case: ft_AC_shuffle_humaneval_mistral_conc20 / task 55

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ok`


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
    "ft": 26
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 20
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
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
program fib_demo
  implicit none
  integer :: n, result

  ! Read input from stdin
  read(*,*) n

  ! Calculate Fibonacci number
  result = fib(n)

  ! Output result to stdout
  print *, result

contains

  recursive function fib(n) result(res)
    integer, intent(in) :: n
    integer :: res
    if (n <= 1) then
      res = n
    else
      res = fib(n-1) + fib(n-2)
    end if
  end function fib

end program fib_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,29 +1,26 @@
-program fibonacci
-    implicit none
-    integer :: n, result
-    integer :: a, b, temp, i
+program fib_demo
+  implicit none
+  integer :: n, result
 
-    ! Read input n
-    read *, n
+  ! Read input from stdin
+  read(*,*) n
 
-    ! Calculate Fibonacci number
-    if (n <= 0) then
-        result = 0
-    else if (n == 1) then
-        result = 1
-    else if (n == 2) then
-        result = 1
+  ! Calculate Fibonacci number
+  result = fib(n)
+
+  ! Output result to stdout
+  print *, result
+
+contains
+
+  recursive function fib(n) result(res)
+    integer, intent(in) :: n
+    integer :: res
+    if (n <= 1) then
+      res = n
     else
-        a = 1
-        b = 1
-        do i = 3, n
-            temp = a + b
-            a = b
-            b = temp
-        end do
-        result = b
+      res = fib(n-1) + fib(n-2)
     end if
+  end function fib
 
-    ! Output result
-    write (*, *) result
-end program fibonacci
+end program fib_demo
```
