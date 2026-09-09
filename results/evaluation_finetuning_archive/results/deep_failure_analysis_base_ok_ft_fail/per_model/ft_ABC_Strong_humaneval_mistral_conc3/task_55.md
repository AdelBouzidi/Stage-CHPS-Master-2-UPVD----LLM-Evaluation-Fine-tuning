# Failure case: ft_ABC_Strong_humaneval_mistral_conc3 / task 55

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
    "ft": 37
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 30
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
  integer :: n
  integer :: result

  ! Read input from stdin
  read(*,*) n

  ! Calculate Fibonacci number
  result = fib(n)

  ! Output result to stdout
  print *, result

contains

  integer function fib(n)
    integer, intent(in) :: n
    integer :: a, b, temp

    if (n <= 0) then
      fib = 0
    else if (n == 1) then
      fib = 1
    else
      a = 0
      b = 1
      do i = 2, n
        temp = a + b
        a = b
        b = temp
      end do
      fib = b
    end if
  end function fib

end program fib_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,29 +1,37 @@
-program fibonacci
-    implicit none
-    integer :: n, result
-    integer :: a, b, temp, i
+program fib_demo
+  implicit none
+  integer :: n
+  integer :: result
 
-    ! Read input n
-    read *, n
+  ! Read input from stdin
+  read(*,*) n
 
-    ! Calculate Fibonacci number
+  ! Calculate Fibonacci number
+  result = fib(n)
+
+  ! Output result to stdout
+  print *, result
+
+contains
+
+  integer function fib(n)
+    integer, intent(in) :: n
+    integer :: a, b, temp
+
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
+      a = 0
+      b = 1
+      do i = 2, n
+        temp = a + b
+        a = b
+        b = temp
+      end do
+      fib = b
     end if
+  end function fib
 
-    ! Output result
-    write (*, *) result
-end program fibonacci
+end program fib_demo
```
