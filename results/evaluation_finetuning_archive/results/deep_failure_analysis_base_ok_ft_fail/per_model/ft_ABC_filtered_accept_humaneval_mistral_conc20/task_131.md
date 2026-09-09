# Failure case: ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 131

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
  "uses_read_stdin": {
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
  read(*,*) n
  result = digits(n)
  print *, result
contains
  function digits(n) result(res)
    integer, intent(in) :: n
    integer :: res
    integer :: i, digit
    res = 0
    do i = 1, n
      digit = mod(i, 10)
      if (mod(digit, 2) == 1) then
        res = res * digit
      end if
    end do
  end function digits
end program digits
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,20 @@
-program odd_digit_product
-    implicit none
-    integer :: n, digit, product
-    integer :: temp
-    logical :: found_odd
-
-    ! Read input
-    read *, n
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
+program digits
+  implicit none
+  integer :: n, result
+  read(*,*) n
+  result = digits(n)
+  print *, result
+contains
+  function digits(n) result(res)
+    integer, intent(in) :: n
+    integer :: res
+    integer :: i, digit
+    res = 0
+    do i = 1, n
+      digit = mod(i, 10)
+      if (mod(digit, 2) == 1) then
+        res = res * digit
+      end if
     end do
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
+  end function digits
+end program digits
```
