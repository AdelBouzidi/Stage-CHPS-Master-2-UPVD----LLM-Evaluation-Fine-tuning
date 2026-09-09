# Failure case: ft_B_humaneval_mistral_conc20 / task 36

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `status_ok`


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
  "num_lines": {
    "base": 30,
    "ft": 25
  },
  "num_nonempty_lines": {
    "base": 25,
    "ft": 22
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
program count_sevens
  implicit none
  integer :: n, i, count, num, digit
  integer :: result

  read *, n

  result = 0
  do i = 1, n - 1
    if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
      count = 0
      num = i
      do while (num > 0)
        digit = mod(num, 10)
        if (digit == 7) then
          count = count + 1
        end if
        num = num / 10
      end do
      result = result + count
    end if
  end do

  print *, result
end program count_sevens
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,30 +1,25 @@
 program count_sevens
-    implicit none
-    integer :: n, i, count, num, digit
+  implicit none
+  integer :: n, i, count, num, digit
+  integer :: result
 
-    ! Read input n from stdin
-    read *, n
+  read *, n
 
-    ! Initialize count
-    count = 0
+  result = 0
+  do i = 1, n - 1
+    if (mod(i, 11) == 0 .or. mod(i, 13) == 0) then
+      count = 0
+      num = i
+      do while (num > 0)
+        digit = mod(num, 10)
+        if (digit == 7) then
+          count = count + 1
+        end if
+        num = num / 10
+      end do
+      result = result + count
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
+  print *, result
 end program count_sevens
```
