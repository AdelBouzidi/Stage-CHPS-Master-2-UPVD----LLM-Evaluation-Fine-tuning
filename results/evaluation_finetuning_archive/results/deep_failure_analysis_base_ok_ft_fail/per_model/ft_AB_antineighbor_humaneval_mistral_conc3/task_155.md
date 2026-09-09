# Failure case: ft_AB_antineighbor_humaneval_mistral_conc3 / task 155

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_compile_err`


## Prompt

```text
Write a Fortran90 program that, given an integer, returns a tuple (pair) containing the count of even digits and the count of odd digits in the integer.
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
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 39,
    "ft": 31
  },
  "num_nonempty_lines": {
    "base": 33,
    "ft": 25
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
program even_odd_count
    implicit none
    integer :: num
    integer :: even_count, odd_count
    integer :: digit
    integer :: temp
    
    ! Read input
    read *, num
    
    ! Handle negative numbers by taking absolute value
    if (num < 0) then
        temp = -num
    else
        temp = num
    end if
    
    ! Count even and odd digits
    even_count = 0
    odd_count = 0
    
    if (temp == 0) then
        even_count = 1  ! 0 is even
    else
        do while (temp > 0)
            digit = mod(temp, 10)
            if (mod(digit, 2) == 0) then
                even_count = even_count + 1
            else
                odd_count = odd_count + 1
            end if
            temp = temp / 10
        end do
    end if
    
    ! Output results
    write (*, *) even_count, odd_count
    
end program even_odd_count
```


## FT generated code

```fortran
program even_odd_count_demo
  implicit none
  integer :: num
  integer :: even_count, odd_count
  character(len=1) :: digit

  ! Read input number
  read(*,*) num

  ! Initialize counters
  even_count = 0
  odd_count = 0

  ! Convert to absolute value for digit processing
  num = abs(num)

  ! Process each digit
  do while (num > 0)
    digit = char(mod(num, 10) + 48)
    if (mod(digit, 2) == 0) then
      even_count = even_count + 1
    else
      odd_count = odd_count + 1
    end if
    num = num / 10
  end do

  ! Output results
  print *, even_count, odd_count

end program even_odd_count_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,39 +1,31 @@
-program even_odd_count
-    implicit none
-    integer :: num
-    integer :: even_count, odd_count
-    integer :: digit
-    integer :: temp
-    
-    ! Read input
-    read *, num
-    
-    ! Handle negative numbers by taking absolute value
-    if (num < 0) then
-        temp = -num
+program even_odd_count_demo
+  implicit none
+  integer :: num
+  integer :: even_count, odd_count
+  character(len=1) :: digit
+
+  ! Read input number
+  read(*,*) num
+
+  ! Initialize counters
+  even_count = 0
+  odd_count = 0
+
+  ! Convert to absolute value for digit processing
+  num = abs(num)
+
+  ! Process each digit
+  do while (num > 0)
+    digit = char(mod(num, 10) + 48)
+    if (mod(digit, 2) == 0) then
+      even_count = even_count + 1
     else
-        temp = num
+      odd_count = odd_count + 1
     end if
-    
-    ! Count even and odd digits
-    even_count = 0
-    odd_count = 0
-    
-    if (temp == 0) then
-        even_count = 1  ! 0 is even
-    else
-        do while (temp > 0)
-            digit = mod(temp, 10)
-            if (mod(digit, 2) == 0) then
-                even_count = even_count + 1
-            else
-                odd_count = odd_count + 1
-            end if
-            temp = temp / 10
-        end do
-    end if
-    
-    ! Output results
-    write (*, *) even_count, odd_count
-    
-end program even_odd_count
+    num = num / 10
+  end do
+
+  ! Output results
+  print *, even_count, odd_count
+
+end program even_odd_count_demo
```
