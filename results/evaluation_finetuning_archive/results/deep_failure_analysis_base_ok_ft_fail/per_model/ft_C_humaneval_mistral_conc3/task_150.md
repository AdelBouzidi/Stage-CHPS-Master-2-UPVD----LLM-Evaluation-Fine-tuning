# Failure case: ft_C_humaneval_mistral_conc3 / task 150

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ineq`


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
    "ft": 46
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 39
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
  integer :: n, x, y, result

  ! Read input
  read(*,*) n
  read(*,*) x
  read(*,*) y

  ! Check if n is prime
  if (is_prime(n)) then
    result = x
  else
    result = y
  end if

  ! Output result
  print *, result

contains

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
      do while (i*i <= n)
        if (mod(n, i) == 0) then
          prime = .false.
          exit
        end if
        i = i + 1
      end do
    end if
  end function is_prime

end program x_or_y
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,46 @@
 program x_or_y
+  implicit none
+  integer :: n, x, y, result
+
+  ! Read input
+  read(*,*) n
+  read(*,*) x
+  read(*,*) y
+
+  ! Check if n is prime
+  if (is_prime(n)) then
+    result = x
+  else
+    result = y
+  end if
+
+  ! Output result
+  print *, result
+
+contains
+
+  function is_prime(n) result(prime)
     implicit none
-    integer :: n, x, y
+    integer, intent(in) :: n
+    logical :: prime
     integer :: i
-    logical :: is_prime
-    
-    ! Read input
-    read *, n
-    read *, x
-    read *, y
-    
-    ! Check if n is prime
-    is_prime = .true.
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
+      do while (i*i <= n)
+        if (mod(n, i) == 0) then
+          prime = .false.
+          exit
+        end if
+        i = i + 1
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
