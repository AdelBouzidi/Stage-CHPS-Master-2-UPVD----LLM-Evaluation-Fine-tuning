# Failure case: ft_AB_antineighbor_humaneval_mistral_conc3 / task 131

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_output_labels`

- Labels: `static_modifies_intent_in_possible, static_output_labels, status_compile_err`


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
    "base": 33,
    "ft": 38
  },
  "num_nonempty_lines": {
    "base": 27,
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
    integer :: i, digit, product
    character(len=10) :: num_str

    ! Convert number to string
    write(num_str, '(I0)') n

    ! Calculate product of odd digits
    product = 1
    do i = 1, len(num_str)
      digit = iachar(num_str(i:i)) - iachar('0')
      if (mod(digit, 2) == 1) then
        product = product * digit
      end if
    end do

    res = product
  end function digits

end program digits
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,38 @@
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
+    integer :: i, digit, product
+    character(len=10) :: num_str
 
-    ! Read input
-    read *, n
+    ! Convert number to string
+    write(num_str, '(I0)') n
 
-    ! Initialize variables
-    temp = n
+    ! Calculate product of odd digits
     product = 1
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
+    do i = 1, len(num_str)
+      digit = iachar(num_str(i:i)) - iachar('0')
+      if (mod(digit, 2) == 1) then
+        product = product * digit
+      end if
     end do
 
-    ! If no odd digits found, result is 0
-    if (.not. found_odd) then
-        product = 0
-    end if
+    res = product
+  end function digits
 
-    ! Output result
-    write (*, *) product
-
-end program odd_digit_product
+end program digits
```
