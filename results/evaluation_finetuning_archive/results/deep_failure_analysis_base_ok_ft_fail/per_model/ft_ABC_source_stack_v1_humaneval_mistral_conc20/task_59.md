# Failure case: ft_ABC_source_stack_v1_humaneval_mistral_conc20 / task 59

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `status_ok`


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
    "ft": 40
  },
  "num_nonempty_lines": {
    "base": 28,
    "ft": 34
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
program main
  implicit none
  integer :: n, i, largest
  integer :: temp

  ! Read input
  read *, n

  ! Find largest prime factor
  largest = 2
  temp = n

  ! Check for factor 2
  if (mod(temp, 2) == 0) then
    largest = 2
    do while (mod(temp, 2) == 0)
      temp = temp / 2
    end do
  end if

  ! Check for odd factors
  i = 3
  do while (i * i <= temp)
    if (mod(temp, i) == 0) then
      largest = i
      do while (mod(temp, i) == 0)
        temp = temp / i
      end do
    end if
    i = i + 2
  end do

  ! If temp > 1, then it's a prime factor
  if (temp > 1) then
    largest = temp
  end if

  ! Output result
  print *, largest
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,35 +1,40 @@
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
+program main
+  implicit none
+  integer :: n, i, largest
+  integer :: temp
+
+  ! Read input
+  read *, n
+
+  ! Find largest prime factor
+  largest = 2
+  temp = n
+
+  ! Check for factor 2
+  if (mod(temp, 2) == 0) then
+    largest = 2
+    do while (mod(temp, 2) == 0)
+      temp = temp / 2
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
-    if (n > 1) then
-        largest_factor = n
+  end if
+
+  ! Check for odd factors
+  i = 3
+  do while (i * i <= temp)
+    if (mod(temp, i) == 0) then
+      largest = i
+      do while (mod(temp, i) == 0)
+        temp = temp / i
+      end do
     end if
-    
-    ! Output result to stdout
-    write (*, *) largest_factor
-    
-end program largest_prime_factor
+    i = i + 2
+  end do
+
+  ! If temp > 1, then it's a prime factor
+  if (temp > 1) then
+    largest = temp
+  end if
+
+  ! Output result
+  print *, largest
+end program main
```
