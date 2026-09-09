# Failure case: ft_C_humaneval_mistral_conc20 / task 49

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ineq`


## Prompt

```text
Write a Fortran90 program that computes 2 raised to the power n modulo p.
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
    "base": 22,
    "ft": 9
  },
  "num_nonempty_lines": {
    "base": 19,
    "ft": 8
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
program modp
  implicit none
  integer :: n, p, result, base
  
  ! Read input
  read *, n
  read *, p
  
  ! Compute 2^n mod p using modular exponentiation
  result = 1
  base = 2
  do while (n > 0)
    if (mod(n, 2) == 1) then
      result = mod(result * base, p)
    end if
    base = mod(base * base, p)
    n = n / 2
  end do
  
  ! Output result
  write (*, *) result
end program modp
```


## FT generated code

```fortran
program modp
  implicit none
  integer :: n, p, result

  read(*,*) n, p
  result = 2**n
  result = mod(result, p)
  print *, result
end program modp
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,22 +1,9 @@
 program modp
   implicit none
-  integer :: n, p, result, base
-  
-  ! Read input
-  read *, n
-  read *, p
-  
-  ! Compute 2^n mod p using modular exponentiation
-  result = 1
-  base = 2
-  do while (n > 0)
-    if (mod(n, 2) == 1) then
-      result = mod(result * base, p)
-    end if
-    base = mod(base * base, p)
-    n = n / 2
-  end do
-  
-  ! Output result
-  write (*, *) result
+  integer :: n, p, result
+
+  read(*,*) n, p
+  result = 2**n
+  result = mod(result, p)
+  print *, result
 end program modp
```
