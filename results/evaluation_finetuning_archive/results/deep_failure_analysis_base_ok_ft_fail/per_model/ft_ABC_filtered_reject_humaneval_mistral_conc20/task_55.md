# Failure case: ft_ABC_filtered_reject_humaneval_mistral_conc20 / task 55

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
  "num_lines": {
    "base": 29,
    "ft": 18
  },
  "num_nonempty_lines": {
    "base": 26,
    "ft": 15
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
  integer, dimension(100) :: fib

  ! Initialize Fibonacci array
  fib(1) = 1
  fib(2) = 1
  do i = 3, 100
    fib(i) = fib(i-1) + fib(i-2)
  end do

  ! Read input
  read(*,*) n

  ! Output result
  print *, fib(n)
end program fib_demo
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
+program fib_demo
+  implicit none
+  integer :: n, result
+  integer, dimension(100) :: fib
 
-    ! Read input n
-    read *, n
+  ! Initialize Fibonacci array
+  fib(1) = 1
+  fib(2) = 1
+  do i = 3, 100
+    fib(i) = fib(i-1) + fib(i-2)
+  end do
 
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
+  ! Read input
+  read(*,*) n
 
-    ! Output result
-    write (*, *) result
-end program fibonacci
+  ! Output result
+  print *, fib(n)
+end program fib_demo
```
