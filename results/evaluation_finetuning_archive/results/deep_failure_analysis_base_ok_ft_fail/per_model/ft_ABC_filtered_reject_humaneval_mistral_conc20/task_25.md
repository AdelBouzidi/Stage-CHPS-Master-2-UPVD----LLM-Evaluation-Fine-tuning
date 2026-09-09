# Failure case: ft_ABC_filtered_reject_humaneval_mistral_conc20 / task 25

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_stdin_read, status_compile_err`


## Prompt

```text
Write a Fortran90 program that returns an array of prime factors of a given integer in the order from smallest to largest, listing each factor as many times as it appears in the factorization.
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
    "base": 45,
    "ft": 14
  },
  "num_nonempty_lines": {
    "base": 38,
    "ft": 11
  },
  "uses_allocatable": {
    "base": false,
    "ft": true
  },
  "uses_assumed_shape": {
    "base": false,
    "ft": true
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program prime_factors
    implicit none
    integer :: n
    integer :: i
    integer, dimension(100) :: factors
    integer :: count
    integer :: temp

    ! Read input
    read(*,*) n

    ! Handle edge cases
    if (n <= 1) then
        write(*,*)
        stop
    end if

    ! Initialize count
    count = 0

    ! Find prime factors
    temp = n
    i = 2
    do while (i * i <= temp)
        do while (mod(temp, i) == 0)
            count = count + 1
            factors(count) = i
            temp = temp / i
        end do
        i = i + 1
    end do

    ! If temp > 1, then it's a prime factor
    if (temp > 1) then
        count = count + 1
        factors(count) = temp
    end if

    ! Output the factors
    do i = 1, count
        if (i > 1) write(*,*) ' '
        write(*,*) factors(i)
    end do

end program prime_factors
```


## FT generated code

```fortran
program main
  implicit none
  integer :: n
  integer, allocatable :: factors(:)
  
  ! Read input
  read(*,*) n
  
  ! Call factorize
  call factorize(n, factors)
  
  ! Output result
  write(*,*) factors
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,45 +1,14 @@
-program prime_factors
-    implicit none
-    integer :: n
-    integer :: i
-    integer, dimension(100) :: factors
-    integer :: count
-    integer :: temp
-
-    ! Read input
-    read(*,*) n
-
-    ! Handle edge cases
-    if (n <= 1) then
-        write(*,*)
-        stop
-    end if
-
-    ! Initialize count
-    count = 0
-
-    ! Find prime factors
-    temp = n
-    i = 2
-    do while (i * i <= temp)
-        do while (mod(temp, i) == 0)
-            count = count + 1
-            factors(count) = i
-            temp = temp / i
-        end do
-        i = i + 1
-    end do
-
-    ! If temp > 1, then it's a prime factor
-    if (temp > 1) then
-        count = count + 1
-        factors(count) = temp
-    end if
-
-    ! Output the factors
-    do i = 1, count
-        if (i > 1) write(*,*) ' '
-        write(*,*) factors(i)
-    end do
-
-end program prime_factors
+program main
+  implicit none
+  integer :: n
+  integer, allocatable :: factors(:)
+  
+  ! Read input
+  read(*,*) n
+  
+  ! Call factorize
+  call factorize(n, factors)
+  
+  ! Output result
+  write(*,*) factors
+end program main
```
