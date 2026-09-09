# Failure case: ft_AC_shuffle_humaneval_mistral_conc20 / task 59

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


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
    "base": 35,
    "ft": 36
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 29
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
program largest_prime_factor
  implicit none
  integer :: n, result

  ! Read input number
  read *, n

  ! Calculate largest prime factor
  result = largest_prime_factor(n)

  ! Output result
  print *, result

contains

  function largest_prime_factor(n) result(res)
    integer, intent(in) :: n
    integer :: res
    integer :: i

    res = 2
    i = 2
    do while (i * i <= n)
      if (mod(n, i) == 0) then
        res = i
        n = n / i
      else
        i = i + 1
      end if
    end do
    if (n > 1) then
      res = n
    end if
  end function largest_prime_factor

end program largest_prime_factor
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,35 +1,36 @@
 program largest_prime_factor
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
+  implicit none
+  integer :: n, result
+
+  ! Read input number
+  read *, n
+
+  ! Calculate largest prime factor
+  result = largest_prime_factor(n)
+
+  ! Output result
+  print *, result
+
+contains
+
+  function largest_prime_factor(n) result(res)
+    integer, intent(in) :: n
+    integer :: res
+    integer :: i
+
+    res = 2
+    i = 2
+    do while (i * i <= n)
+      if (mod(n, i) == 0) then
+        res = i
+        n = n / i
+      else
+        i = i + 1
+      end if
     end do
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
     if (n > 1) then
-        largest_factor = n
+      res = n
     end if
-    
-    ! Output result to stdout
-    write (*, *) largest_factor
-    
+  end function largest_prime_factor
+
 end program largest_prime_factor
```
