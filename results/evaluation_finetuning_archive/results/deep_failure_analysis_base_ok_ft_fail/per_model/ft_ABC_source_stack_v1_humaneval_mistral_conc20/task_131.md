# Failure case: ft_ABC_source_stack_v1_humaneval_mistral_conc20 / task 131

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `status_ineq`

- Labels: `status_ineq`


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
  "num_lines": {
    "base": 33,
    "ft": 26
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 21
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
program main
  implicit none
  integer :: n, result, digit
  integer :: product

  read *, n

  result = 0
  product = 1
  do while (n > 0)
    digit = mod(n, 10)
    if (mod(digit, 2) == 1) then
      product = product * digit
    end if
    n = n / 10
  end do

  if (product == 1) then
    result = 0
  else
    result = product
  end if

  print *, result

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,26 @@
-program odd_digit_product
-    implicit none
-    integer :: n, digit, product
-    integer :: temp
-    logical :: found_odd
+program main
+  implicit none
+  integer :: n, result, digit
+  integer :: product
 
-    ! Read input
-    read *, n
+  read *, n
 
-    ! Initialize variables
-    temp = n
-    product = 1
-    found_odd = .false.
+  result = 0
+  product = 1
+  do while (n > 0)
+    digit = mod(n, 10)
+    if (mod(digit, 2) == 1) then
+      product = product * digit
+    end if
+    n = n / 10
+  end do
 
-    ! Process each digit
-    do while (temp > 0)
-        digit = mod(temp, 10)
-        if (mod(digit, 2) == 1) then
-            product = product * digit
-            found_odd = .true.
-        end if
-        temp = temp / 10
-    end do
+  if (product == 1) then
+    result = 0
+  else
+    result = product
+  end if
 
-    ! If no odd digits found, result is 0
-    if (.not. found_odd) then
-        product = 0
-    end if
+  print *, result
 
-    ! Output result
-    write (*, *) product
-
-end program odd_digit_product
+end program main
```
