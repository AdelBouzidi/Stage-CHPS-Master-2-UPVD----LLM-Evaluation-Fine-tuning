# Failure case: ft_ABC_source_stack_v2_humaneval_mistral_conc20 / task 131

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ineq`


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
  "num_lines": {
    "base": 33,
    "ft": 21
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 17
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
  integer :: i, digit, product

  ! Read input
  read(*,*) n

  ! Calculate product of odd digits
  product = 0
  do i = 1, n
    digit = mod(i, 10)
    if (mod(digit, 2) == 1) then
      product = product * digit
    end if
  end do

  ! Output result
  print *, product

end program digits
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,33 +1,21 @@
-program odd_digit_product
-    implicit none
-    integer :: n, digit, product
-    integer :: temp
-    logical :: found_odd
+program digits
+  implicit none
+  integer :: n, result
+  integer :: i, digit, product
 
-    ! Read input
-    read *, n
+  ! Read input
+  read(*,*) n
 
-    ! Initialize variables
-    temp = n
-    product = 1
-    found_odd = .false.
+  ! Calculate product of odd digits
+  product = 0
+  do i = 1, n
+    digit = mod(i, 10)
+    if (mod(digit, 2) == 1) then
+      product = product * digit
+    end if
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
+  ! Output result
+  print *, product
 
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
