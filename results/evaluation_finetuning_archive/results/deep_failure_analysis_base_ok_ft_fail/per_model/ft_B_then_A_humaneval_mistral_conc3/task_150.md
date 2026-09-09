# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 150

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


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
    "ft": 4
  },
  "num_lines": {
    "base": 32,
    "ft": 38
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 33
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
program x_or_y
  implicit none
  integer :: n, x, y
  integer :: result

  read *, n
  read *, x
  read *, y
  result = x_or_y(n, x, y)
  print *, result

contains

  integer function x_or_y(n, x, y)
    integer, intent(in) :: n, x, y
    if (prime(n)) then
      x_or_y = x
    else
      x_or_y = y
    end if
  end function x_or_y

  integer function prime(n)
    integer, intent(in) :: n
    prime = .true.
    if (n < 2) then
      prime = .false.
    else
      do i = 2, n-1
        if (mod(n, i) == 0) then
          prime = .false.
          exit
        end if
      end do
    end if
  end function prime

end program x_or_y
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,38 @@
 program x_or_y
-    implicit none
-    integer :: n, x, y
-    integer :: i
-    logical :: is_prime
-    
-    ! Read input
-    read *, n
-    read *, x
-    read *, y
-    
-    ! Check if n is prime
-    is_prime = .true.
-    if (n <= 1) then
-        is_prime = .false.
+  implicit none
+  integer :: n, x, y
+  integer :: result
+
+  read *, n
+  read *, x
+  read *, y
+  result = x_or_y(n, x, y)
+  print *, result
+
+contains
+
+  integer function x_or_y(n, x, y)
+    integer, intent(in) :: n, x, y
+    if (prime(n)) then
+      x_or_y = x
     else
-        do i = 2, int(sqrt(real(n)))
-            if (mod(n, i) == 0) then
-                is_prime = .false.
-                exit
-            end if
-        end do
+      x_or_y = y
     end if
-    
-    ! Output result
-    if (is_prime) then
-        print *, x
+  end function x_or_y
+
+  integer function prime(n)
+    integer, intent(in) :: n
+    prime = .true.
+    if (n < 2) then
+      prime = .false.
     else
-        print *, y
+      do i = 2, n-1
+        if (mod(n, i) == 0) then
+          prime = .false.
+          exit
+        end if
+      end do
     end if
-    
+  end function prime
+
 end program x_or_y
```
