# Failure case: ft_ABC_filtered_manual_humaneval_mistral_conc20 / task 123

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that returns a sorted array containing the odd numbers present in the Collatz sequence of a given positive integer.
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
    "base": 60,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 53,
    "ft": 0
  },
  "uses_allocatable": {
    "base": true,
    "ft": false
  },
  "uses_allocate": {
    "base": true,
    "ft": false
  },
  "uses_assumed_shape": {
    "base": true,
    "ft": false
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  },
  "uses_implicit_none": {
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
program collatz_odds
    implicit none
    integer :: n
    integer, allocatable :: odd_collatz(:)
    integer :: i, j, temp, count

    ! Read input
    read *, n

    ! Collect odd numbers from Collatz sequence
    count = 0
    temp = n
    do while (temp > 0)
        if (mod(temp, 2) == 1) then
            count = count + 1
        end if
        if (temp == 1) exit
        if (mod(temp, 2) == 0) then
            temp = temp / 2
        else
            temp = 3 * temp + 1
        end if
    end do

    ! Allocate array for odd numbers
    allocate(odd_collatz(count))
    count = 0

    ! Collect odd numbers again
    temp = n
    do while (temp > 0)
        if (mod(temp, 2) == 1) then
            count = count + 1
            odd_collatz(count) = temp
        end if
        if (temp == 1) exit
        if (mod(temp, 2) == 0) then
            temp = temp / 2
        else
            temp = 3 * temp + 1
        end if
    end do

    ! Sort the odd numbers using bubble sort
    do i = 1, count - 1
        do j = i + 1, count
            if (odd_collatz(i) > odd_collatz(j)) then
                odd_collatz(i) = odd_collatz(i) + odd_collatz(j)
                odd_collatz(j) = odd_collatz(i) - odd_collatz(j)
                odd_collatz(i) = odd_collatz(i) - odd_collatz(j)
            end if
        end do
    end do

    ! Output the sorted odd numbers
    do i = 1, count
        write (*, '(I0)') odd_collatz(i)
    end do

end program collatz_odds
```


## FT generated code

```fortran

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,60 +0,0 @@
-program collatz_odds
-    implicit none
-    integer :: n
-    integer, allocatable :: odd_collatz(:)
-    integer :: i, j, temp, count
-
-    ! Read input
-    read *, n
-
-    ! Collect odd numbers from Collatz sequence
-    count = 0
-    temp = n
-    do while (temp > 0)
-        if (mod(temp, 2) == 1) then
-            count = count + 1
-        end if
-        if (temp == 1) exit
-        if (mod(temp, 2) == 0) then
-            temp = temp / 2
-        else
-            temp = 3 * temp + 1
-        end if
-    end do
-
-    ! Allocate array for odd numbers
-    allocate(odd_collatz(count))
-    count = 0
-
-    ! Collect odd numbers again
-    temp = n
-    do while (temp > 0)
-        if (mod(temp, 2) == 1) then
-            count = count + 1
-            odd_collatz(count) = temp
-        end if
-        if (temp == 1) exit
-        if (mod(temp, 2) == 0) then
-            temp = temp / 2
-        else
-            temp = 3 * temp + 1
-        end if
-    end do
-
-    ! Sort the odd numbers using bubble sort
-    do i = 1, count - 1
-        do j = i + 1, count
-            if (odd_collatz(i) > odd_collatz(j)) then
-                odd_collatz(i) = odd_collatz(i) + odd_collatz(j)
-                odd_collatz(j) = odd_collatz(i) - odd_collatz(j)
-                odd_collatz(i) = odd_collatz(i) - odd_collatz(j)
-            end if
-        end do
-    end do
-
-    ! Output the sorted odd numbers
-    do i = 1, count
-        write (*, '(I0)') odd_collatz(i)
-    end do
-
-end program collatz_odds
```
