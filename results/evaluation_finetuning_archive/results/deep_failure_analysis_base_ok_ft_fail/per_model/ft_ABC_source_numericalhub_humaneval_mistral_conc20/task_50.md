# Failure case: ft_ABC_source_numericalhub_humaneval_mistral_conc20 / task 50

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ok`


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
    "base": 32,
    "ft": 31
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 26
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
program decode_shift_demo
  implicit none
  character(len=3) :: input_str
  character(len=3) :: output_str
  
  read(*, '(a)') input_str
  output_str = decode_shift(input_str)
  print *, output_str
  
contains

  function decode_shift(s) result(res)
    implicit none
    character(len=*), intent(in) :: s
    character(len=len(s)) :: res
    integer :: i
    character(len=1) :: c
    
    do i = 1, len(s)
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        res(i:i) = char(ichar(c) - 5)
      else if (c >= 'A' .and. c <= 'Z') then
        res(i:i) = char(ichar(c) - 5)
      else
        res(i:i) = c
      end if
    end do
  end function decode_shift

end program decode_shift_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,31 @@
-program decode_shift
+program decode_shift_demo
+  implicit none
+  character(len=3) :: input_str
+  character(len=3) :: output_str
+  
+  read(*, '(a)') input_str
+  output_str = decode_shift(input_str)
+  print *, output_str
+  
+contains
+
+  function decode_shift(s) result(res)
     implicit none
-    character(len=100) :: input_str
-    character(len=100) :: result
+    character(len=*), intent(in) :: s
+    character(len=len(s)) :: res
     integer :: i
-    integer :: char_code
-    integer :: shifted_code
+    character(len=1) :: c
     
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
+    do i = 1, len(s)
+      c = s(i:i)
+      if (c >= 'a' .and. c <= 'z') then
+        res(i:i) = char(ichar(c) - 5)
+      else if (c >= 'A' .and. c <= 'Z') then
+        res(i:i) = char(ichar(c) - 5)
+      else
+        res(i:i) = c
+      end if
     end do
-    
-    print *, result
-end program decode_shift
+  end function decode_shift
+
+end program decode_shift_demo
```
