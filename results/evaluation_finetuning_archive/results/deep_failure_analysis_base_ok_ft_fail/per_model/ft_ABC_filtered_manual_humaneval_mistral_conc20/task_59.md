# Failure case: ft_ABC_filtered_manual_humaneval_mistral_conc20 / task 59

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that returns the largest prime factor of a given number. Assume the number is greater than 1 and is not a prime.
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
    "base": 35,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 28,
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
program largest_prime_factor
    implicit none
    integer :: n, i, largest_factor
    
    ! Read input from stdin
    read *, n
    
    ! Initialize largest_factor
    largest_factor = 2
    
    ! Check for factor 2
    do while (mod(n, 2) == 0)
        n = n / 2
        largest_factor = 2
    end do
    
    ! Check for odd factors starting from 3
    i = 3
    do while (i * i <= n)
        do while (mod(n, i) == 0)
            n = n / i
            largest_factor = i
        end do
        i = i + 2
    end do
    
    ! If n > 1, then n is a prime factor
    if (n > 1) then
        largest_factor = n
    end if
    
    ! Output result to stdout
    write (*, *) largest_factor
    
end program largest_prime_factor
```


## FT generated code

```fortran

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,35 +0,0 @@
-program largest_prime_factor
-    implicit none
-    integer :: n, i, largest_factor
-    
-    ! Read input from stdin
-    read *, n
-    
-    ! Initialize largest_factor
-    largest_factor = 2
-    
-    ! Check for factor 2
-    do while (mod(n, 2) == 0)
-        n = n / 2
-        largest_factor = 2
-    end do
-    
-    ! Check for odd factors starting from 3
-    i = 3
-    do while (i * i <= n)
-        do while (mod(n, i) == 0)
-            n = n / i
-            largest_factor = i
-        end do
-        i = i + 2
-    end do
-    
-    ! If n > 1, then n is a prime factor
-    if (n > 1) then
-        largest_factor = n
-    end if
-    
-    ! Output result to stdout
-    write (*, *) largest_factor
-    
-end program largest_prime_factor
```
