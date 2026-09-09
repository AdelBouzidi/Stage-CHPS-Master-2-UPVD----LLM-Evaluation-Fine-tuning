# Failure case: ft_C_humaneval_mistral_conc3 / task 36

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that returns the number of times the digit 7 appears in integers less than n which are divisible by 11 or 13.
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
  "has_debug_words": {
    "base": true,
    "ft": false
  },
  "has_program": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 30,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 25,
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
  "uses_write_star": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program count_sevens
    implicit none
    integer :: n, i, count, num, digit

    ! Read input n from stdin
    read *, n

    ! Initialize count
    count = 0

    ! Loop through numbers less than n
    do i = 1, n - 1
        ! Check if divisible by 11 or 13
        if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
            ! Count occurrences of digit 7 in this number
            num = i
            do while (num > 0)
                digit = mod(num, 10)
                if (digit == 7) then
                    count = count + 1
                end if
                num = num / 10
            end do
        end if
    end do

    ! Output result to stdout
    write (*, *) count

end program count_sevens
```


## FT generated code

```fortran

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,30 +0,0 @@
-program count_sevens
-    implicit none
-    integer :: n, i, count, num, digit
-
-    ! Read input n from stdin
-    read *, n
-
-    ! Initialize count
-    count = 0
-
-    ! Loop through numbers less than n
-    do i = 1, n - 1
-        ! Check if divisible by 11 or 13
-        if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
-            ! Count occurrences of digit 7 in this number
-            num = i
-            do while (num > 0)
-                digit = mod(num, 10)
-                if (digit == 7) then
-                    count = count + 1
-                end if
-                num = num / 10
-            end do
-        end if
-    end do
-
-    ! Output result to stdout
-    write (*, *) count
-
-end program count_sevens
```
