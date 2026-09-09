# Failure case: ft_ABC_source_numerical_methods_humaneval_mistral_conc20 / task 25

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ok`


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
  "num_lines": {
    "base": 45,
    "ft": 40
  },
  "num_nonempty_lines": {
    "base": 38,
    "ft": 34
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
    integer, dimension(100) :: factors
    integer :: count
    
    ! Read input
    read(*,*) n
    
    ! Handle edge cases
    if (n <= 1) then
        write(*,*)
        stop
    end if
    
    ! Find prime factors
    count = 0
    i = 2
    do while (i * i <= n)
        do while (mod(n, i) == 0)
            count = count + 1
            factors(count) = i
            n = n / i
        end do
        i = i + 1
    end do
    
    ! If n > 1, then the remaining n is prime
    if (n > 1) then
        count = count + 1
        factors(count) = n
    end if
    
    ! Output the factors
    do i = 1, count
        if (i > 1) write(*,*) ' '
        write(*,*) factors(i)
    end do
    
end program prime_factors
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,45 +1,40 @@
 program prime_factors
     implicit none
-    integer :: n
-    integer :: i
+    integer :: n, i
     integer, dimension(100) :: factors
     integer :: count
-    integer :: temp
-
+    
     ! Read input
     read(*,*) n
-
+    
     ! Handle edge cases
     if (n <= 1) then
         write(*,*)
         stop
     end if
-
-    ! Initialize count
+    
+    ! Find prime factors
     count = 0
-
-    ! Find prime factors
-    temp = n
     i = 2
-    do while (i * i <= temp)
-        do while (mod(temp, i) == 0)
+    do while (i * i <= n)
+        do while (mod(n, i) == 0)
             count = count + 1
             factors(count) = i
-            temp = temp / i
+            n = n / i
         end do
         i = i + 1
     end do
-
-    ! If temp > 1, then it's a prime factor
-    if (temp > 1) then
+    
+    ! If n > 1, then the remaining n is prime
+    if (n > 1) then
         count = count + 1
-        factors(count) = temp
+        factors(count) = n
     end if
-
+    
     ! Output the factors
     do i = 1, count
         if (i > 1) write(*,*) ' '
         write(*,*) factors(i)
     end do
-
+    
 end program prime_factors
```
