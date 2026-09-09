# Failure case: ft_AB_shuffle_humaneval_mistral_conc15 / task 31

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_output_labels`

- Labels: `static_modifies_intent_in_possible, static_output_labels, status_ineq`


## Prompt

```text
Write a Fortran90 program that returns true if a given number is prime, and false otherwise.
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
  "has_labels_in_output": {
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
    "base": 33,
    "ft": 40
  },
  "num_nonempty_lines": {
    "base": 30,
    "ft": 32
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
program is_prime_check
    implicit none
    integer :: n
    integer :: i
    logical :: result
    real :: sqrt_n

    ! Read input number
    read *, n

    ! Check if prime
    result = .true.
    if (n <= 1) then
        result = .false.
    else if (n == 2) then
        result = .true.
    else if (n == 3) then
        result = .true.
    else if (mod(n, 2) == 0) then
        result = .false.
    else
        sqrt_n = sqrt(real(n))
        do i = 3, int(sqrt_n) + 1, 2
            if (mod(n, i) == 0) then
                result = .false.
                exit
            end if
        end do
    end if

    ! Output result
    write (*, '(L)') result
end program is_prime_check
```


## FT generated code

```fortran
program is_prime_demo
  implicit none
  integer :: n
  logical :: result

  ! Hardcoded input value
  n = 6

  result = is_prime(n)

  print *, 'is_prime(', n, ') =', result

contains

  logical function is_prime(n)
    implicit none
    integer, intent(in) :: n
    integer :: i
    logical :: prime

    if (n <= 1) then
      prime = .false.
    else if (n == 2) then
      prime = .true.
    else if (mod(n, 2) == 0) then
      prime = .false.
    else
      prime = .true.
      do i = 3, int(sqrt(real(n))), 2
        if (mod(n, i) == 0) then
          prime = .false.
          exit
        end if
      end do
    end if

    is_prime = prime
  end function is_prime

end program is_prime_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,40 @@
-program is_prime_check
+program is_prime_demo
+  implicit none
+  integer :: n
+  logical :: result
+
+  ! Hardcoded input value
+  n = 6
+
+  result = is_prime(n)
+
+  print *, 'is_prime(', n, ') =', result
+
+contains
+
+  logical function is_prime(n)
     implicit none
-    integer :: n
+    integer, intent(in) :: n
     integer :: i
-    logical :: result
-    real :: sqrt_n
+    logical :: prime
 
-    ! Read input number
-    read *, n
-
-    ! Check if prime
-    result = .true.
     if (n <= 1) then
-        result = .false.
+      prime = .false.
     else if (n == 2) then
-        result = .true.
-    else if (n == 3) then
-        result = .true.
+      prime = .true.
     else if (mod(n, 2) == 0) then
-        result = .false.
+      prime = .false.
     else
-        sqrt_n = sqrt(real(n))
-        do i = 3, int(sqrt_n) + 1, 2
-            if (mod(n, i) == 0) then
-                result = .false.
-                exit
-            end if
-        end do
+      prime = .true.
+      do i = 3, int(sqrt(real(n))), 2
+        if (mod(n, i) == 0) then
+          prime = .false.
+          exit
+        end if
+      end do
     end if
 
-    ! Output result
-    write (*, '(L)') result
-end program is_prime_check
+    is_prime = prime
+  end function is_prime
+
+end program is_prime_demo
```
