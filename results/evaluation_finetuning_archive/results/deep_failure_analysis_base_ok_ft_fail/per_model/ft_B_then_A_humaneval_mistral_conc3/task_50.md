# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 50

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that takes as input a string encoded with the encode_shift function (which shifts every character by 5 in the alphabet) and returns the decoded string.
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
  "num_functions": {
    "base": 0,
    "ft": 2
  },
  "num_lines": {
    "base": 32,
    "ft": 26
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 24
  },
  "uses_print_star": {
    "base": true,
    "ft": false
  },
  "uses_write_star": {
    "base": false,
    "ft": true
  }
}
```


## Base generated code

```fortran
program decode_shift
    implicit none
    character(len=100) :: input_str
    character(len=100) :: result
    integer :: i
    integer :: char_code
    integer :: shifted_code
    
    read *, input_str
    
    result = input_str
    
    do i = 1, len_trim(input_str)
        char_code = iachar(input_str(i:i))
        
        if (char_code >= ichar('a') .and. char_code <= ichar('z')) then
            shifted_code = char_code - 5
            if (shifted_code < ichar('a')) then
                shifted_code = shifted_code + 26
            end if
            result(i:i) = achar(shifted_code)
        else if (char_code >= ichar('A') .and. char_code <= ichar('Z')) then
            shifted_code = char_code - 5
            if (shifted_code < ichar('A')) then
                shifted_code = shifted_code + 26
            end if
            result(i:i) = achar(shifted_code)
        end if
    end do
    
    print *, result
end program decode_shift
```


## FT generated code

```fortran
program main
        implicit none
        character(len=100) :: s
        character(len=100) :: result
        integer :: i

        function decode_shift(string s)
        implicit none
        character(len=100) :: s
        character(len=100) :: decode_shift
        integer :: i
        do i = 1, len(s)
            if (s(i:i) >= 'a' .and. s(i:i) <= 'z') then
                decode_shift = char(ieor(s(i:i), 5))
            else if (s(i:i) >= 'A' .and. s(i:i) <= 'Z') then
                decode_shift = char(ieor(s(i:i), 5))
            else
                decode_shift = s(i:i)
            end if
        end do
        end function decode_shift

        read *, s
        result = decode_shift(s)
        write (*, '(A)') result
        end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,26 @@
-program decode_shift
-    implicit none
-    character(len=100) :: input_str
-    character(len=100) :: result
-    integer :: i
-    integer :: char_code
-    integer :: shifted_code
-    
-    read *, input_str
-    
-    result = input_str
-    
-    do i = 1, len_trim(input_str)
-        char_code = iachar(input_str(i:i))
-        
-        if (char_code >= ichar('a') .and. char_code <= ichar('z')) then
-            shifted_code = char_code - 5
-            if (shifted_code < ichar('a')) then
-                shifted_code = shifted_code + 26
+program main
+        implicit none
+        character(len=100) :: s
+        character(len=100) :: result
+        integer :: i
+
+        function decode_shift(string s)
+        implicit none
+        character(len=100) :: s
+        character(len=100) :: decode_shift
+        integer :: i
+        do i = 1, len(s)
+            if (s(i:i) >= 'a' .and. s(i:i) <= 'z') then
+                decode_shift = char(ieor(s(i:i), 5))
+            else if (s(i:i) >= 'A' .and. s(i:i) <= 'Z') then
+                decode_shift = char(ieor(s(i:i), 5))
+            else
+                decode_shift = s(i:i)
             end if
-            result(i:i) = achar(shifted_code)
-        else if (char_code >= ichar('A') .and. char_code <= ichar('Z')) then
-            shifted_code = char_code - 5
-            if (shifted_code < ichar('A')) then
-                shifted_code = shifted_code + 26
-            end if
-            result(i:i) = achar(shifted_code)
-        end if
-    end do
-    
-    print *, result
-end program decode_shift
+        end do
+        end function decode_shift
+
+        read *, s
+        result = decode_shift(s)
+        write (*, '(A)') result
+        end program main
```
