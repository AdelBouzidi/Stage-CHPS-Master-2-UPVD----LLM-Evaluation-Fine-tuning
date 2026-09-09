# Failure case: ft_A_humaneval_mistral_conc20 / task 49

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
  "has_contains": {
    "base": false,
    "ft": true
  },
  "modifies_intent_in_possible": {
    "base": false,
    "ft": true
  },
  "num_functions": {
    "base": 0,
    "ft": 2
  },
  "num_lines": {
    "base": 22,
    "ft": 26
  },
  "num_nonempty_lines": {
    "base": 19,
    "ft": 20
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
program modp_demo
  implicit none
  integer :: n, p, result

  ! Read input
  read(*,*) n, p

  ! Compute 2^n mod p
  result = modp(n, p)

  ! Output result
  print *, result

contains

  integer function modp(n, p)
    integer, intent(in) :: n, p
    integer :: i, result
    result = 1
    do i = 1, n
      result = (result * 2) mod p
    end do
    modp = result
  end function modp

end program modp_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,22 +1,26 @@
-program modp
+program modp_demo
   implicit none
-  integer :: n, p, result, base
-  
+  integer :: n, p, result
+
   ! Read input
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
+  read(*,*) n, p
+
+  ! Compute 2^n mod p
+  result = modp(n, p)
+
   ! Output result
-  write (*, *) result
-end program modp
+  print *, result
+
+contains
+
+  integer function modp(n, p)
+    integer, intent(in) :: n, p
+    integer :: i, result
+    result = 1
+    do i = 1, n
+      result = (result * 2) mod p
+    end do
+    modp = result
+  end function modp
+
+end program modp_demo
```
