# Failure case: ft_AC_antineighbor_humaneval_mistral_conc20 / task 59

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `status_ineq`

- Labels: `status_ineq`


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
  "num_lines": {
    "base": 35,
    "ft": 21
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 17
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
  integer :: n, i, largest_factor

  ! Read input number
  read *, n

  ! Find largest prime factor
  largest_factor = 2
  do i = 2, n
    if (mod(n, i) == 0) then
      largest_factor = i
      n = n / i
      if (n == 1) exit
    end if
  end do

  ! Output result
  print *, largest_factor

end program largest_prime_factor
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,35 +1,21 @@
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
+  implicit none
+  integer :: n, i, largest_factor
+
+  ! Read input number
+  read *, n
+
+  ! Find largest prime factor
+  largest_factor = 2
+  do i = 2, n
+    if (mod(n, i) == 0) then
+      largest_factor = i
+      n = n / i
+      if (n == 1) exit
     end if
-    
-    ! Output result to stdout
-    write (*, *) largest_factor
-    
+  end do
+
+  ! Output result
+  print *, largest_factor
+
 end program largest_prime_factor
```
