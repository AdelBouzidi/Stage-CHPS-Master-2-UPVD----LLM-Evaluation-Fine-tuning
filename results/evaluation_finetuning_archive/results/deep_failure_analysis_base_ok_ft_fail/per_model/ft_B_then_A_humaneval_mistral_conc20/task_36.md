# Failure case: ft_B_then_A_humaneval_mistral_conc20 / task 36

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ok`


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
  "has_debug_words": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 30,
    "ft": 22
  },
  "num_nonempty_lines": {
    "base": 25,
    "ft": 19
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
  integer :: n, i, count, temp

  ! Read input n
  read(*, *) n

  count = 0
  do i = 1, n-1
    if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
      temp = i
      do while (temp /= 0)
        if (mod(temp, 10) == 7) then
          count = count + 1
        end if
        temp = temp / 10
      end do
    end if
  end do

  print *, count
end program fizz_buzz
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,30 +1,22 @@
-program count_sevens
-    implicit none
-    integer :: n, i, count, num, digit
+program fizz_buzz
+  implicit none
+  integer :: n, i, count, temp
 
-    ! Read input n from stdin
-    read *, n
+  ! Read input n
+  read(*, *) n
 
-    ! Initialize count
-    count = 0
+  count = 0
+  do i = 1, n-1
+    if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
+      temp = i
+      do while (temp /= 0)
+        if (mod(temp, 10) == 7) then
+          count = count + 1
+        end if
+        temp = temp / 10
+      end do
+    end if
+  end do
 
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
+  print *, count
+end program fizz_buzz
```
