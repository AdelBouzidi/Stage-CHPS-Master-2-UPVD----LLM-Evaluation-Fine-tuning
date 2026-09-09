# Failure case: ft_ABC_source_stack_v1_humaneval_mistral_conc20 / task 155

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ok`


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
    "ft": 35
  },
  "num_nonempty_lines": {
    "base": 33,
    "ft": 29
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
program main
  implicit none
  integer :: num
  integer :: even_count, odd_count
  integer :: digit
  integer :: temp

  read(*,*) num

  if (num < 0) then
    temp = -num
  else
    temp = num
  end if

  even_count = 0
  odd_count = 0

  if (temp == 0) then
    even_count = 1
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

  print *, even_count, odd_count

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,39 +1,35 @@
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
-    else
-        temp = num
-    end if
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
+program main
+  implicit none
+  integer :: num
+  integer :: even_count, odd_count
+  integer :: digit
+  integer :: temp
+
+  read(*,*) num
+
+  if (num < 0) then
+    temp = -num
+  else
+    temp = num
+  end if
+
+  even_count = 0
+  odd_count = 0
+
+  if (temp == 0) then
+    even_count = 1
+  else
+    do while (temp > 0)
+      digit = mod(temp, 10)
+      if (mod(digit, 2) == 0) then
+        even_count = even_count + 1
+      else
+        odd_count = odd_count + 1
+      end if
+      temp = temp / 10
+    end do
+  end if
+
+  print *, even_count, odd_count
+
+end program main
```
