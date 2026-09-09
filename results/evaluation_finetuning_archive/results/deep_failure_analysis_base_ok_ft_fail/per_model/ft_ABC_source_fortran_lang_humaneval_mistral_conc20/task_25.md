# Failure case: ft_ABC_source_fortran_lang_humaneval_mistral_conc20 / task 25

- Base status: `ok`

- FT status: `runtime_err`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_output_labels, status_runtime_err`


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
  "has_labels_in_output": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 45,
    "ft": 38
  },
  "num_nonempty_lines": {
    "base": 38,
    "ft": 32
  },
  "uses_allocatable": {
    "base": false,
    "ft": true
  },
  "uses_assumed_shape": {
    "base": false,
    "ft": true
  },
  "uses_read_stdin": {
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
program prime_factors
    implicit none
    integer :: n, i
    integer, allocatable :: factors(:)
    integer :: factor_count
    
    ! Read input
    read *, n
    
    ! Initialize factors array
    factor_count = 0
    
    ! Find prime factors
    i = 2
    do while (i * i <= n)
        do while (mod(n, i) == 0)
            factor_count = factor_count + 1
            factors(factor_count) = i
            n = n / i
        end do
        i = i + 1
    end do
    
    ! If n > 1, then the remaining n is a prime factor
    if (n > 1) then
        factor_count = factor_count + 1
        factors(factor_count) = n
    end if
    
    ! Output the factors
    if (factor_count > 0) then
        do i = 1, factor_count
            write (*, '(I0)') factors(i)
            if (i < factor_count) write (*, '(A)') ' '
        end do
    end if
    
end program prime_factors
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,45 +1,38 @@
 program prime_factors
     implicit none
-    integer :: n
-    integer :: i
-    integer, dimension(100) :: factors
-    integer :: count
-    integer :: temp
-
+    integer :: n, i
+    integer, allocatable :: factors(:)
+    integer :: factor_count
+    
     ! Read input
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
+    read *, n
+    
+    ! Initialize factors array
+    factor_count = 0
+    
     ! Find prime factors
-    temp = n
     i = 2
-    do while (i * i <= temp)
-        do while (mod(temp, i) == 0)
-            count = count + 1
-            factors(count) = i
-            temp = temp / i
+    do while (i * i <= n)
+        do while (mod(n, i) == 0)
+            factor_count = factor_count + 1
+            factors(factor_count) = i
+            n = n / i
         end do
         i = i + 1
     end do
-
-    ! If temp > 1, then it's a prime factor
-    if (temp > 1) then
-        count = count + 1
-        factors(count) = temp
+    
+    ! If n > 1, then the remaining n is a prime factor
+    if (n > 1) then
+        factor_count = factor_count + 1
+        factors(factor_count) = n
     end if
-
+    
     ! Output the factors
-    do i = 1, count
-        if (i > 1) write(*,*) ' '
-        write(*,*) factors(i)
-    end do
-
+    if (factor_count > 0) then
+        do i = 1, factor_count
+            write (*, '(I0)') factors(i)
+            if (i < factor_count) write (*, '(A)') ' '
+        end do
+    end if
+    
 end program prime_factors
```
