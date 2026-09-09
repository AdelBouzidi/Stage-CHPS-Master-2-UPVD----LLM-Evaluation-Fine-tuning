# Failure case: ft_AB_antineighbor_humaneval_mistral_conc3 / task 150

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `status_ineq`

- Labels: `static_modifies_intent_in_possible, status_ineq`


## Prompt

```text
Write a Fortran90 program that returns the value of x if n is a prime number and returns the value of y otherwise.
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
  "has_debug_words": {
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
    "base": 32,
    "ft": 42
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 34
  }
}
```


## Base generated code

```fortran
program x_or_y
    implicit none
    integer :: n, x, y
    integer :: i
    logical :: is_prime
    
    ! Read input
    read *, n
    read *, x
    read *, y
    
    ! Check if n is prime
    is_prime = .true.
    if (n <= 1) then
        is_prime = .false.
    else
        do i = 2, int(sqrt(real(n)))
            if (mod(n, i) == 0) then
                is_prime = .false.
                exit
            end if
        end do
    end if
    
    ! Output result
    if (is_prime) then
        print *, x
    else
        print *, y
    end if
    
end program x_or_y
```


## FT generated code

```fortran
program x_or_y_demo
  implicit none
  integer :: n, x, y, result

  ! Hardcoded input values
  n = 7
  x = 34
  y = 12

  result = x_or_y(n, x, y)

  print *, result

contains

  function x_or_y(n, x, y) result(res)
    implicit none
    integer, intent(in) :: n, x, y
    integer :: res
    integer :: i
    logical :: is_prime

    is_prime = .true.
    if (n < 2) then
      is_prime = .false.
    else
      do i = 2, n - 1
        if (mod(n, i) == 0) then
          is_prime = .false.
          exit
        end if
      end do
    end if

    if (is_prime) then
      res = x
    else
      res = y
    end if
  end function x_or_y

end program x_or_y_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,42 @@
-program x_or_y
+program x_or_y_demo
+  implicit none
+  integer :: n, x, y, result
+
+  ! Hardcoded input values
+  n = 7
+  x = 34
+  y = 12
+
+  result = x_or_y(n, x, y)
+
+  print *, result
+
+contains
+
+  function x_or_y(n, x, y) result(res)
     implicit none
-    integer :: n, x, y
+    integer, intent(in) :: n, x, y
+    integer :: res
     integer :: i
     logical :: is_prime
-    
-    ! Read input
-    read *, n
-    read *, x
-    read *, y
-    
-    ! Check if n is prime
+
     is_prime = .true.
-    if (n <= 1) then
-        is_prime = .false.
+    if (n < 2) then
+      is_prime = .false.
     else
-        do i = 2, int(sqrt(real(n)))
-            if (mod(n, i) == 0) then
-                is_prime = .false.
-                exit
-            end if
-        end do
+      do i = 2, n - 1
+        if (mod(n, i) == 0) then
+          is_prime = .false.
+          exit
+        end if
+      end do
     end if
-    
-    ! Output result
+
     if (is_prime) then
-        print *, x
+      res = x
     else
-        print *, y
+      res = y
     end if
-    
-end program x_or_y
+  end function x_or_y
+
+end program x_or_y_demo
```
