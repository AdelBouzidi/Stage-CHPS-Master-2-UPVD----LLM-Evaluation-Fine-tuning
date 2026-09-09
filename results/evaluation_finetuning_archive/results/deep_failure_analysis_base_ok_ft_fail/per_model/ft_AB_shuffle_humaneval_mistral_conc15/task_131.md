# Failure case: ft_AB_shuffle_humaneval_mistral_conc15 / task 131

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
  "num_lines": {
    "base": 33,
    "ft": 26
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 22
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

  ! Read input
  read(*,*) n

  ! Calculate product of odd digits
  result = 0
  if (n > 0) then
    result = 1
    do while (n > 0)
      if (mod(n, 10) /= 0) then
        result = result * mod(n, 10)
      else
        result = 0
        exit
      end if
      n = n / 10
    end do
  end if

  ! Output result
  print *, result

end program digits
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
+program digits
+  implicit none
+  integer :: n, result
 
-    ! Read input
-    read *, n
+  ! Read input
+  read(*,*) n
 
-    ! Initialize variables
-    temp = n
-    product = 1
-    found_odd = .false.
+  ! Calculate product of odd digits
+  result = 0
+  if (n > 0) then
+    result = 1
+    do while (n > 0)
+      if (mod(n, 10) /= 0) then
+        result = result * mod(n, 10)
+      else
+        result = 0
+        exit
+      end if
+      n = n / 10
+    end do
+  end if
 
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
+  print *, result
 
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
