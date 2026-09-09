# Failure case: ft_AB_antineighbor_humaneval_mistral_conc20 / task 131

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
    "base": 33,
    "ft": 42
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 35
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
  integer :: n, result

  ! Read input
  read *, n

  ! Calculate result
  result = digits(n)

  ! Output result
  print *, result

contains

  function digits(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: i, digit, product, has_odd

    res = 0
    product = 1
    has_odd = 0
    i = 0
    do while (n > 0)
      digit = mod(n, 10)
      if (mod(digit, 2) == 1) then
        product = product * digit
        has_odd = 1
      end if
      n = n / 10
      i = i + 1
    end do
    if (has_odd == 1) then
      res = product
    else
      res = 0
    end if
  end function digits

end program digits
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,42 @@
-program odd_digit_product
+program digits
+  implicit none
+  integer :: n, result
+
+  ! Read input
+  read *, n
+
+  ! Calculate result
+  result = digits(n)
+
+  ! Output result
+  print *, result
+
+contains
+
+  function digits(n) result(res)
     implicit none
-    integer :: n, digit, product
-    integer :: temp
-    logical :: found_odd
+    integer, intent(in) :: n
+    integer :: res
+    integer :: i, digit, product, has_odd
 
-    ! Read input
-    read *, n
+    res = 0
+    product = 1
+    has_odd = 0
+    i = 0
+    do while (n > 0)
+      digit = mod(n, 10)
+      if (mod(digit, 2) == 1) then
+        product = product * digit
+        has_odd = 1
+      end if
+      n = n / 10
+      i = i + 1
+    end do
+    if (has_odd == 1) then
+      res = product
+    else
+      res = 0
+    end if
+  end function digits
 
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
+end program digits
```
