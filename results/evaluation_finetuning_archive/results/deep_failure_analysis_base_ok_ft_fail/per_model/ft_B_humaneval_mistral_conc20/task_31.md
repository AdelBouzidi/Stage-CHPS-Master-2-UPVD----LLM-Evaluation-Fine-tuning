# Failure case: ft_B_humaneval_mistral_conc20 / task 31

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `status_ok`


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
program is_prime
  implicit none
  integer :: n
  logical :: result
  integer :: i

  read *, n

  if (n <= 1) then
    result = .false.
  else if (n == 2) then
    result = .true.
  else if (mod(n, 2) == 0) then
    result = .false.
  else
    result = .true.
    i = 3
    do while (result .and. i * i <= n)
      if (mod(n, i) == 0) then
        result = .false.
      end if
      i = i + 2
    end do
  end if

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
-    integer :: i
-    logical :: result
-    real :: sqrt_n
+program is_prime
+  implicit none
+  integer :: n
+  logical :: result
+  integer :: i
 
-    ! Read input number
-    read *, n
+  read *, n
 
-    ! Check if prime
+  if (n <= 1) then
+    result = .false.
+  else if (n == 2) then
     result = .true.
-    if (n <= 1) then
+  else if (mod(n, 2) == 0) then
+    result = .false.
+  else
+    result = .true.
+    i = 3
+    do while (result .and. i * i <= n)
+      if (mod(n, i) == 0) then
         result = .false.
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
+      end if
+      i = i + 2
+    end do
+  end if
 
-    ! Output result
-    write (*, '(L)') result
-end program is_prime_check
+  print *, result
+end program is_prime
```
