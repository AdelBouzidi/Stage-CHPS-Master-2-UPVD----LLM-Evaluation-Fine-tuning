# Failure case: ft_ABC_filtered_manual_humaneval_mistral_conc20 / task 25

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


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
  "has_program": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 45,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 38,
    "ft": 0
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  },
  "uses_implicit_none": {
    "base": true,
    "ft": false
  },
  "uses_read_stdin": {
    "base": true,
    "ft": false
  },
  "uses_write_star": {
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

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,45 +0,0 @@
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
```
