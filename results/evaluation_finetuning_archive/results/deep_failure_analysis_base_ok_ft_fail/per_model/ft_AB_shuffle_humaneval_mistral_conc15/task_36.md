# Failure case: ft_AB_shuffle_humaneval_mistral_conc15 / task 36

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
    "ft": 2
  },
  "num_lines": {
    "base": 30,
    "ft": 35
  },
  "num_nonempty_lines": {
    "base": 25,
    "ft": 28
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
    implicit none
    integer, intent(in) :: n
    integer :: i, temp

    fizz_buzz = 0
    do i = 1, n-1
      if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
        temp = i
        do while (temp > 0)
          if (mod(temp, 10) == 7) then
            fizz_buzz = fizz_buzz + 1
          end if
          temp = temp / 10
        end do
      end if
    end do
  end function fizz_buzz

end program fizz_buzz
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,30 +1,35 @@
-program count_sevens
+program fizz_buzz
+  implicit none
+  integer :: n, result
+
+  ! Read input from stdin
+  read(*,*) n
+
+  ! Calculate the result
+  result = fizz_buzz(n)
+
+  ! Output the result
+  print *, result
+
+contains
+
+  integer function fizz_buzz(n)
     implicit none
-    integer :: n, i, count, num, digit
+    integer, intent(in) :: n
+    integer :: i, temp
 
-    ! Read input n from stdin
-    read *, n
+    fizz_buzz = 0
+    do i = 1, n-1
+      if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
+        temp = i
+        do while (temp > 0)
+          if (mod(temp, 10) == 7) then
+            fizz_buzz = fizz_buzz + 1
+          end if
+          temp = temp / 10
+        end do
+      end if
+    end do
+  end function fizz_buzz
 
-    ! Initialize count
-    count = 0
-
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
-
-    ! Output result to stdout
-    write (*, *) count
-
-end program count_sevens
+end program fizz_buzz
```
