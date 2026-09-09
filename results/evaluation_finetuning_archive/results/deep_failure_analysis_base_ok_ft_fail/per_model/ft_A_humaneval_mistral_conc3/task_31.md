# Failure case: ft_A_humaneval_mistral_conc3 / task 31

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_compile_err`


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
  "num_lines": {
    "base": 33,
    "ft": 14
  },
  "num_nonempty_lines": {
    "base": 30,
    "ft": 11
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
program main
  implicit none
  integer :: n
  logical :: result

  ! Read input from stdin
  read(*,*) n

  ! Call the is_prime function
  result = is_prime(n)

  ! Output the result
  print *, result
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,14 @@
-program is_prime_check
-    implicit none
-    integer :: n
-    integer :: i
-    logical :: result
-    real :: sqrt_n
+program main
+  implicit none
+  integer :: n
+  logical :: result
 
-    ! Read input number
-    read *, n
+  ! Read input from stdin
+  read(*,*) n
 
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
+  ! Call the is_prime function
+  result = is_prime(n)
 
-    ! Output result
-    write (*, '(L)') result
-end program is_prime_check
+  ! Output the result
+  print *, result
+end program main
```
