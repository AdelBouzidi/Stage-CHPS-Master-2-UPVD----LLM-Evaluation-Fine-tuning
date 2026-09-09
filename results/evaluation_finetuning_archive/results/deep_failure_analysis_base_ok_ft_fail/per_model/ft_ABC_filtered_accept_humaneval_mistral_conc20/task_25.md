# Failure case: ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 25

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
  "has_contains": {
    "base": false,
    "ft": true
  },
  "has_debug_words": {
    "base": false,
    "ft": true
  },
  "modifies_intent_in_possible": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 45,
    "ft": 54
  },
  "num_nonempty_lines": {
    "base": 38,
    "ft": 44
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
  },
  "uses_allocatable": {
    "base": false,
    "ft": true
  },
  "uses_allocate": {
    "base": false,
    "ft": true
  },
  "uses_assumed_shape": {
    "base": false,
    "ft": true
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
program factorize_demo
  implicit none
  integer :: n
  integer, allocatable :: factors(:)
  
  ! Read input
  read(*,*) n
  
  ! Call factorize function
  call factorize(n, factors)
  
  ! Print output
  print *, factors
  
contains

  subroutine factorize(n, factors)
    implicit none
    integer, intent(in) :: n
    integer, intent(out), allocatable :: factors(:)
    integer :: i, count
    integer, allocatable :: temp(:)
    
    ! Initialize factors array
    allocate(temp(1))
    temp(1) = 1
    count = 1
    
    ! Find prime factors
    do i = 2, n
      if (mod(n, i) == 0) then
        count = 0
        do while (mod(n, i) == 0)
          count = count + 1
          n = n / i
        end do
        allocate(temp(count))
        temp(1:count) = i
        factors = temp
        exit
      end if
    end do
    
    ! If n > 1, it's a prime factor
    if (n > 1) then
      allocate(temp(1))
      temp(1) = n
      factors = temp
    end if
    
    deallocate(temp)
  end subroutine factorize

end program factorize_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,45 +1,54 @@
-program prime_factors
+program factorize_demo
+  implicit none
+  integer :: n
+  integer, allocatable :: factors(:)
+  
+  ! Read input
+  read(*,*) n
+  
+  ! Call factorize function
+  call factorize(n, factors)
+  
+  ! Print output
+  print *, factors
+  
+contains
+
+  subroutine factorize(n, factors)
     implicit none
-    integer :: n
-    integer :: i
-    integer, dimension(100) :: factors
-    integer :: count
-    integer :: temp
+    integer, intent(in) :: n
+    integer, intent(out), allocatable :: factors(:)
+    integer :: i, count
+    integer, allocatable :: temp(:)
+    
+    ! Initialize factors array
+    allocate(temp(1))
+    temp(1) = 1
+    count = 1
+    
+    ! Find prime factors
+    do i = 2, n
+      if (mod(n, i) == 0) then
+        count = 0
+        do while (mod(n, i) == 0)
+          count = count + 1
+          n = n / i
+        end do
+        allocate(temp(count))
+        temp(1:count) = i
+        factors = temp
+        exit
+      end if
+    end do
+    
+    ! If n > 1, it's a prime factor
+    if (n > 1) then
+      allocate(temp(1))
+      temp(1) = n
+      factors = temp
+    end if
+    
+    deallocate(temp)
+  end subroutine factorize
 
-    ! Read input
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
-    ! Find prime factors
-    temp = n
-    i = 2
-    do while (i * i <= temp)
-        do while (mod(temp, i) == 0)
-            count = count + 1
-            factors(count) = i
-            temp = temp / i
-        end do
-        i = i + 1
-    end do
-
-    ! If temp > 1, then it's a prime factor
-    if (temp > 1) then
-        count = count + 1
-        factors(count) = temp
-    end if
-
-    ! Output the factors
-    do i = 1, count
-        if (i > 1) write(*,*) ' '
-        write(*,*) factors(i)
-    end do
-
-end program prime_factors
+end program factorize_demo
```
