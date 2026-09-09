# Failure case: ft_C_humaneval_mistral_conc3 / task 31

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_possible_zero_indexing`

- Labels: `static_possible_zero_indexing, static_stdin_read, status_compile_err`


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
    "ft": 27
  },
  "num_nonempty_lines": {
    "base": 30,
    "ft": 24
  },
  "uses_array_index_0_literal": {
    "base": false,
    "ft": true
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
program is_prime
  implicit none
  integer :: n
  logical :: result

  ! Read input
  read(*,*) n

  ! Check if prime
  result = .true.
  if (n <= 1) result = .false.
  if (n == 2) result = .true.
  if (n == 3) result = .true.
  if (n > 3 .and. mod(n, 2) == 0) result = .false.
  if (n > 3) then
    integer :: i
    do i = 3, sqrt(real(n), kind=real(0))
      if (mod(n, i) == 0) then
        result = .false.
        exit
      end if
    end do
  end if

  ! Output result
  print *, result
end program is_prime
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,27 @@
-program is_prime_check
-    implicit none
-    integer :: n
+program is_prime
+  implicit none
+  integer :: n
+  logical :: result
+
+  ! Read input
+  read(*,*) n
+
+  ! Check if prime
+  result = .true.
+  if (n <= 1) result = .false.
+  if (n == 2) result = .true.
+  if (n == 3) result = .true.
+  if (n > 3 .and. mod(n, 2) == 0) result = .false.
+  if (n > 3) then
     integer :: i
-    logical :: result
-    real :: sqrt_n
+    do i = 3, sqrt(real(n), kind=real(0))
+      if (mod(n, i) == 0) then
+        result = .false.
+        exit
+      end if
+    end do
+  end if
 
-    ! Read input number
-    read *, n
-
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
+  ! Output result
+  print *, result
+end program is_prime
```
