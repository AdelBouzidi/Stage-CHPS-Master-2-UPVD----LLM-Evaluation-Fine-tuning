# Failure case: ft_AB_shuffle_humaneval_mistral_conc15 / task 150

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
    "ft": 56
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 47
  },
  "uses_read_stdin": {
    "base": false,
    "ft": true
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

  ! Read input values
  read(*,*) n
  read(*,*) x
  read(*,*) y

  ! Call the function
  result = x_or_y(n, x, y)

  ! Output the result
  print *, result

contains

  function x_or_y(n, x, y) result(res)
    implicit none
    integer, intent(in) :: n, x, y
    integer :: res
    integer :: i

    ! Check if n is prime
    if (is_prime(n)) then
      res = x
    else
      res = y
    end if
  end function x_or_y

  function is_prime(n) result(prime)
    implicit none
    integer, intent(in) :: n
    logical :: prime
    integer :: i

    if (n <= 1) then
      prime = .false.
    else if (n == 2) then
      prime = .true.
    else if (mod(n, 2) == 0) then
      prime = .false.
    else
      prime = .true.
      do i = 3, int(sqrt(real(n))) + 1, 2
        if (mod(n, i) == 0) then
          prime = .false.
          exit
        end if
      end do
    end if
  end function is_prime

end program x_or_y
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,56 @@
 program x_or_y
+  implicit none
+  integer :: n, x, y
+  integer :: result
+
+  ! Read input values
+  read(*,*) n
+  read(*,*) x
+  read(*,*) y
+
+  ! Call the function
+  result = x_or_y(n, x, y)
+
+  ! Output the result
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
-    logical :: is_prime
-    
-    ! Read input
-    read *, n
-    read *, x
-    read *, y
-    
+
     ! Check if n is prime
-    is_prime = .true.
+    if (is_prime(n)) then
+      res = x
+    else
+      res = y
+    end if
+  end function x_or_y
+
+  function is_prime(n) result(prime)
+    implicit none
+    integer, intent(in) :: n
+    logical :: prime
+    integer :: i
+
     if (n <= 1) then
-        is_prime = .false.
+      prime = .false.
+    else if (n == 2) then
+      prime = .true.
+    else if (mod(n, 2) == 0) then
+      prime = .false.
     else
-        do i = 2, int(sqrt(real(n)))
-            if (mod(n, i) == 0) then
-                is_prime = .false.
-                exit
-            end if
-        end do
+      prime = .true.
+      do i = 3, int(sqrt(real(n))) + 1, 2
+        if (mod(n, i) == 0) then
+          prime = .false.
+          exit
+        end if
+      end do
     end if
-    
-    ! Output result
-    if (is_prime) then
-        print *, x
-    else
-        print *, y
-    end if
-    
+  end function is_prime
+
 end program x_or_y
```
