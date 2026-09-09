# Failure case: ft_AC_shuffle_humaneval_mistral_conc20 / task 36

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


## Prompt

```text
Write a Fortran90 program that returns the number of times the digit 7 appears in integers less than n which are divisible by 11 or 13.
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
    "ft": 3
  },
  "num_lines": {
    "base": 30,
    "ft": 38
  },
  "num_nonempty_lines": {
    "base": 25,
    "ft": 30
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
program count_sevens
    implicit none
    integer :: n, i, count, num, digit

    ! Read input n from stdin
    read *, n

    ! Initialize count
    count = 0

    ! Loop through numbers less than n
    do i = 1, n - 1
        ! Check if divisible by 11 or 13
        if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
            ! Count occurrences of digit 7 in this number
            num = i
            do while (num > 0)
                digit = mod(num, 10)
                if (digit == 7) then
                    count = count + 1
                end if
                num = num / 10
            end do
        end if
    end do

    ! Output result to stdout
    write (*, *) count

end program count_sevens
```


## FT generated code

```fortran
program fizz_buzz
  implicit none
  integer :: n, result

  ! Read input from stdin
  read(*,*) n

  ! Calculate the result
  result = fizz_buzz(n)

  ! Output the result
  print *, result

contains

  integer function fizz_buzz(n)
    integer, intent(in) :: n
    integer :: i, count
    character(len=10) :: num_str

    count = 0
    do i = 1, n-1
      if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
        num_str = i_char(i)
        if (index(num_str, '7') > 0) then
          count = count + 1
        end if
      end if
    end do
    fizz_buzz = count
  end function fizz_buzz

  character(len=10) function i_char(i)
    integer, intent(in) :: i
    write(i_char, '(I0)') i
  end function i_char

end program fizz_buzz
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,30 +1,38 @@
-program count_sevens
-    implicit none
-    integer :: n, i, count, num, digit
+program fizz_buzz
+  implicit none
+  integer :: n, result
 
-    ! Read input n from stdin
-    read *, n
+  ! Read input from stdin
+  read(*,*) n
 
-    ! Initialize count
+  ! Calculate the result
+  result = fizz_buzz(n)
+
+  ! Output the result
+  print *, result
+
+contains
+
+  integer function fizz_buzz(n)
+    integer, intent(in) :: n
+    integer :: i, count
+    character(len=10) :: num_str
+
     count = 0
+    do i = 1, n-1
+      if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
+        num_str = i_char(i)
+        if (index(num_str, '7') > 0) then
+          count = count + 1
+        end if
+      end if
+    end do
+    fizz_buzz = count
+  end function fizz_buzz
 
-    ! Loop through numbers less than n
-    do i = 1, n - 1
-        ! Check if divisible by 11 or 13
-        if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
-            ! Count occurrences of digit 7 in this number
-            num = i
-            do while (num > 0)
-                digit = mod(num, 10)
-                if (digit == 7) then
-                    count = count + 1
-                end if
-                num = num / 10
-            end do
-        end if
-    end do
+  character(len=10) function i_char(i)
+    integer, intent(in) :: i
+    write(i_char, '(I0)') i
+  end function i_char
 
-    ! Output result to stdout
-    write (*, *) count
-
-end program count_sevens
+end program fizz_buzz
```
