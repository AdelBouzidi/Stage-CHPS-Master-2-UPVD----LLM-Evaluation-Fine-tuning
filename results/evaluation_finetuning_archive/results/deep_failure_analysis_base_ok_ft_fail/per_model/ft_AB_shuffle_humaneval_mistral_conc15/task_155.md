# Failure case: ft_AB_shuffle_humaneval_mistral_conc15 / task 155

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
  "num_lines": {
    "base": 39,
    "ft": 30
  },
  "num_nonempty_lines": {
    "base": 33,
    "ft": 24
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
program even_odd_count
  implicit none
  integer :: num
  integer :: even_count, odd_count
  character(len=1) :: digit
  character(len=10) :: num_str

  ! Read input number
  read(*,*) num

  ! Convert to string to process digits
  write(num_str,*) abs(num)

  even_count = 0
  odd_count = 0

  do i = 1, len(num_str)
    digit = num_str(i:i)
    if (ichar(digit) == ichar('0') .or. ichar(digit) == ichar('2') .or. &
        ichar(digit) == ichar('4') .or. ichar(digit) == ichar('6') .or. &
        ichar(digit) == ichar('8')) then
      even_count = even_count + 1
    else
      odd_count = odd_count + 1
    end if
  end do

  print *, even_count, odd_count

end program even_odd_count
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,39 +1,30 @@
 program even_odd_count
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
+  implicit none
+  integer :: num
+  integer :: even_count, odd_count
+  character(len=1) :: digit
+  character(len=10) :: num_str
+
+  ! Read input number
+  read(*,*) num
+
+  ! Convert to string to process digits
+  write(num_str,*) abs(num)
+
+  even_count = 0
+  odd_count = 0
+
+  do i = 1, len(num_str)
+    digit = num_str(i:i)
+    if (ichar(digit) == ichar('0') .or. ichar(digit) == ichar('2') .or. &
+        ichar(digit) == ichar('4') .or. ichar(digit) == ichar('6') .or. &
+        ichar(digit) == ichar('8')) then
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
+  end do
+
+  print *, even_count, odd_count
+
 end program even_odd_count
```
