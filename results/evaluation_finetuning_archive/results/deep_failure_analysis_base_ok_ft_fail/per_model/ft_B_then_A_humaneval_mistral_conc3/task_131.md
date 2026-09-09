# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 131

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


## Prompt

```text
Write a Fortran90 program that, given a positive integer n, returns the product of the odd digits. Return 0 if all digits are even.
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
  "modifies_intent_in_possible": {
    "base": false,
    "ft": true
  },
  "num_functions": {
    "base": 0,
    "ft": 2
  },
  "num_lines": {
    "base": 33,
    "ft": 20
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 20
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
program odd_digit_product
    implicit none
    integer :: n, digit, product
    integer :: temp
    logical :: found_odd

    ! Read input
    read *, n

    ! Initialize variables
    temp = n
    product = 1
    found_odd = .false.

    ! Process each digit
    do while (temp > 0)
        digit = mod(temp, 10)
        if (mod(digit, 2) == 1) then
            product = product * digit
            found_odd = .true.
        end if
        temp = temp / 10
    end do

    ! If no odd digits found, result is 0
    if (.not. found_odd) then
        product = 0
    end if

    ! Output result
    write (*, *) product

end program odd_digit_product
```


## FT generated code

```fortran
program digits
    implicit none
    integer function digits(n)
    integer, intent(in) :: n
    digits = 0
    if (n == 0) then
    digits = 0
    else
    digits = 1
    do while (n /= 0)
    digits = digits * mod(n, 10)
    n = n / 10
    end do
    end if
    end function digits
    program main
    integer :: n
    read *, n
    print *, digits(n)
    end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,20 @@
-program odd_digit_product
+program digits
     implicit none
-    integer :: n, digit, product
-    integer :: temp
-    logical :: found_odd
-
-    ! Read input
+    integer function digits(n)
+    integer, intent(in) :: n
+    digits = 0
+    if (n == 0) then
+    digits = 0
+    else
+    digits = 1
+    do while (n /= 0)
+    digits = digits * mod(n, 10)
+    n = n / 10
+    end do
+    end if
+    end function digits
+    program main
+    integer :: n
     read *, n
-
-    ! Initialize variables
-    temp = n
-    product = 1
-    found_odd = .false.
-
-    ! Process each digit
-    do while (temp > 0)
-        digit = mod(temp, 10)
-        if (mod(digit, 2) == 1) then
-            product = product * digit
-            found_odd = .true.
-        end if
-        temp = temp / 10
-    end do
-
-    ! If no odd digits found, result is 0
-    if (.not. found_odd) then
-        product = 0
-    end if
-
-    ! Output result
-    write (*, *) product
-
-end program odd_digit_product
+    print *, digits(n)
+    end program main
```
