# Failure case: ft_A_humaneval_mistral_conc20 / task 155

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_output_labels, static_stdin_read, status_ok`


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
  "has_contains": {
    "base": false,
    "ft": true
  },
  "has_labels_in_output": {
    "base": false,
    "ft": true
  },
  "modifies_intent_in_possible": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 39,
    "ft": 48
  },
  "num_nonempty_lines": {
    "base": 33,
    "ft": 40
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
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
  integer, dimension(2) :: result

  ! Read input
  read(*,*) num

  ! Call the function
  call even_odd_count(num, result)

  ! Output the result
  print *, result(1), result(2)

contains

  subroutine even_odd_count(num, result)
    implicit none
    integer, intent(in) :: num
    integer, intent(out) :: result(2)
    integer :: i, digit, abs_num
    integer :: even_cnt, odd_cnt
    character(len=10) :: str

    abs_num = abs(num)
    even_cnt = 0
    odd_cnt = 0

    if (abs_num == 0) then
      result(1) = 1
      result(2) = 0
    else
      write(str, '(i0)') abs_num
      do i = 1, len_trim(str)
        digit = iachar(str(i:i)) - iachar('0')
        if (mod(digit, 2) == 0) then
          even_cnt = even_cnt + 1
        else
          odd_cnt = odd_cnt + 1
        end if
      end do
      result(1) = even_cnt
      result(2) = odd_cnt
    end if
  end subroutine even_odd_count

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,39 +1,48 @@
-program even_odd_count
+program main
+  implicit none
+  integer :: num
+  integer :: even_count, odd_count
+  integer, dimension(2) :: result
+
+  ! Read input
+  read(*,*) num
+
+  ! Call the function
+  call even_odd_count(num, result)
+
+  ! Output the result
+  print *, result(1), result(2)
+
+contains
+
+  subroutine even_odd_count(num, result)
     implicit none
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
+    integer, intent(in) :: num
+    integer, intent(out) :: result(2)
+    integer :: i, digit, abs_num
+    integer :: even_cnt, odd_cnt
+    character(len=10) :: str
+
+    abs_num = abs(num)
+    even_cnt = 0
+    odd_cnt = 0
+
+    if (abs_num == 0) then
+      result(1) = 1
+      result(2) = 0
     else
-        temp = num
+      write(str, '(i0)') abs_num
+      do i = 1, len_trim(str)
+        digit = iachar(str(i:i)) - iachar('0')
+        if (mod(digit, 2) == 0) then
+          even_cnt = even_cnt + 1
+        else
+          odd_cnt = odd_cnt + 1
+        end if
+      end do
+      result(1) = even_cnt
+      result(2) = odd_cnt
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
+  end subroutine even_odd_count
+
+end program main
```
