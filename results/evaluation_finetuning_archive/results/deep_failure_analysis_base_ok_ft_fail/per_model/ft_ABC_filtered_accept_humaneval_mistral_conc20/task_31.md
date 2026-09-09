# Failure case: ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 31

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
    "ft": 33
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
program prime_check
  implicit none
  integer :: n
  logical :: result

  ! Read input
  read(*,*) n

  ! Call the function
  result = is_prime(n)

  ! Output result
  print *, result

contains

  function is_prime(n) result(res)
    implicit none
    integer, intent(in) :: n
    logical :: res
    integer :: i

    if (n < 2) then
      res = .false.
    else if (n == 2) then
      res = .true.
    else if (mod(n, 2) == 0) then
      res = .false.
    else
      res = .true.
      do i = 3, int(sqrt(real(n, kind=real(0, kind=n))))
        if (mod(n, i) == 0) then
          res = .false.
          exit
        end if
      end do
    end if
  end function is_prime

end program prime_check
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,40 @@
-program is_prime_check
+program prime_check
+  implicit none
+  integer :: n
+  logical :: result
+
+  ! Read input
+  read(*,*) n
+
+  ! Call the function
+  result = is_prime(n)
+
+  ! Output result
+  print *, result
+
+contains
+
+  function is_prime(n) result(res)
     implicit none
-    integer :: n
+    integer, intent(in) :: n
+    logical :: res
     integer :: i
-    logical :: result
-    real :: sqrt_n
 
-    ! Read input number
-    read *, n
+    if (n < 2) then
+      res = .false.
+    else if (n == 2) then
+      res = .true.
+    else if (mod(n, 2) == 0) then
+      res = .false.
+    else
+      res = .true.
+      do i = 3, int(sqrt(real(n, kind=real(0, kind=n))))
+        if (mod(n, i) == 0) then
+          res = .false.
+          exit
+        end if
+      end do
+    end if
+  end function is_prime
 
-    ! Check if prime
-    result = .true.
-    if (n <= 1) then
-        result = .false.
-    else if (n == 2) then
-        result = .true.
-    else if (n == 3) then
-        result = .true.
-    else if (mod(n, 2) == 0) then
-        result = .false.
-    else
-        sqrt_n = sqrt(real(n))
-        do i = 3, int(sqrt_n) + 1, 2
-            if (mod(n, i) == 0) then
-                result = .false.
-                exit
-            end if
-        end do
-    end if
-
-    ! Output result
-    write (*, '(L)') result
-end program is_prime_check
+end program prime_check
```
