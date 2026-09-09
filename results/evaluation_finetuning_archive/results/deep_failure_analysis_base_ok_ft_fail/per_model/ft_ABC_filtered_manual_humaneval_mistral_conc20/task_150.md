# Failure case: ft_ABC_filtered_manual_humaneval_mistral_conc20 / task 150

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that returns the value of x if n is a prime number and returns the value of y otherwise.
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
    "base": 32,
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
  "uses_print_star": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program x_or_y
    implicit none
    integer :: n, x, y
    integer :: i
    logical :: is_prime
    
    ! Read input
    read *, n
    read *, x
    read *, y
    
    ! Check if n is prime
    is_prime = .true.
    if (n <= 1) then
        is_prime = .false.
    else
        do i = 2, int(sqrt(real(n)))
            if (mod(n, i) == 0) then
                is_prime = .false.
                exit
            end if
        end do
    end if
    
    ! Output result
    if (is_prime) then
        print *, x
    else
        print *, y
    end if
    
end program x_or_y
```


## FT generated code

```fortran

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +0,0 @@
-program x_or_y
-    implicit none
-    integer :: n, x, y
-    integer :: i
-    logical :: is_prime
-    
-    ! Read input
-    read *, n
-    read *, x
-    read *, y
-    
-    ! Check if n is prime
-    is_prime = .true.
-    if (n <= 1) then
-        is_prime = .false.
-    else
-        do i = 2, int(sqrt(real(n)))
-            if (mod(n, i) == 0) then
-                is_prime = .false.
-                exit
-            end if
-        end do
-    end if
-    
-    ! Output result
-    if (is_prime) then
-        print *, x
-    else
-        print *, y
-    end if
-    
-end program x_or_y
```
