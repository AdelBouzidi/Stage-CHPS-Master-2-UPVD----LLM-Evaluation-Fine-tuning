# Failure case: ft_B_then_A_humaneval_mistral_conc20 / task 50

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_compile_err`


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
  "num_lines": {
    "base": 32,
    "ft": 9
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 8
  },
  "uses_allocatable": {
    "base": false,
    "ft": true
  },
  "uses_read_stdin": {
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
      character(len=*), dimension(:), allocatable :: s
      character(len=*), dimension(:), allocatable :: result

      read(*,*) s
      result = decode_shift(s)
      print *, result
    end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,9 @@
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
-            end if
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
+program main
+      implicit none
+      character(len=*), dimension(:), allocatable :: s
+      character(len=*), dimension(:), allocatable :: result
+
+      read(*,*) s
+      result = decode_shift(s)
+      print *, result
+    end program main
```
