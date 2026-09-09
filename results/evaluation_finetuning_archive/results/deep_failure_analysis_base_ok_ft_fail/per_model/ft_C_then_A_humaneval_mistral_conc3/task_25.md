# Failure case: ft_C_then_A_humaneval_mistral_conc3 / task 25

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_possible_zero_indexing`

- Labels: `static_modifies_intent_in_possible, static_output_labels, static_possible_zero_indexing, status_compile_err`


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
  "has_labels_in_output": {
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
    "base": 45,
    "ft": 50
  },
  "num_nonempty_lines": {
    "base": 38,
    "ft": 42
  },
  "uses_allocatable": {
    "base": false,
    "ft": true
  },
  "uses_allocate": {
    "base": false,
    "ft": true
  },
  "uses_array_index_0_literal": {
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
  "uses_read_stdin": {
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

  ! Hardcoded input value
  n = 8

  ! Call the factorize function
  factors = factorize(n)

  ! Print the result
  print *, 'Factors of', n, ':', factors

contains

  function factorize(n) result(factors)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: factors(:)
    integer :: i, count
    integer :: temp

    if (n <= 1) then
      allocate(factors(0))
      return
    end if

    allocate(factors(0))
    temp = n
    i = 2
    do while (i * i <= temp)
      count = 0
      do while (mod(temp, i) == 0)
        count = count + 1
        temp = temp / i
      end do
      if (count > 0) then
        allocate(factors(size(factors) + count))
        factors(size(factors) + 1 : size(factors) + count) = i
      end if
      i = i + 1
    end do
    if (temp > 1) then
      allocate(factors(size(factors) + 1))
      factors(size(factors) + 1) = temp
    end if
  end function factorize

end program factorize_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,45 +1,50 @@
-program prime_factors
+program factorize_demo
+  implicit none
+  integer :: n
+  integer, allocatable :: factors(:)
+
+  ! Hardcoded input value
+  n = 8
+
+  ! Call the factorize function
+  factors = factorize(n)
+
+  ! Print the result
+  print *, 'Factors of', n, ':', factors
+
+contains
+
+  function factorize(n) result(factors)
     implicit none
-    integer :: n
-    integer :: i
-    integer, dimension(100) :: factors
-    integer :: count
+    integer, intent(in) :: n
+    integer, allocatable :: factors(:)
+    integer :: i, count
     integer :: temp
 
-    ! Read input
-    read(*,*) n
-
-    ! Handle edge cases
     if (n <= 1) then
-        write(*,*)
-        stop
+      allocate(factors(0))
+      return
     end if
 
-    ! Initialize count
-    count = 0
-
-    ! Find prime factors
+    allocate(factors(0))
     temp = n
     i = 2
     do while (i * i <= temp)
-        do while (mod(temp, i) == 0)
-            count = count + 1
-            factors(count) = i
-            temp = temp / i
-        end do
-        i = i + 1
+      count = 0
+      do while (mod(temp, i) == 0)
+        count = count + 1
+        temp = temp / i
+      end do
+      if (count > 0) then
+        allocate(factors(size(factors) + count))
+        factors(size(factors) + 1 : size(factors) + count) = i
+      end if
+      i = i + 1
     end do
+    if (temp > 1) then
+      allocate(factors(size(factors) + 1))
+      factors(size(factors) + 1) = temp
+    end if
+  end function factorize
 
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
