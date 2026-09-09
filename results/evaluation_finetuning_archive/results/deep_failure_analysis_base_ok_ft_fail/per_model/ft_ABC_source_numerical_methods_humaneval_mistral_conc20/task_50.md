# Failure case: ft_ABC_source_numerical_methods_humaneval_mistral_conc20 / task 50

- Base status: `ok`

- FT status: `exception`

- Primary cause: `status_exception`

- Labels: `status_exception`


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
  "has_debug_words": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 32,
    "ft": 33
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 29
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
program decode_shift
    implicit none
    character(len=100) :: encoded
    character(len=100) :: decoded
    integer :: i
    integer :: char_code
    integer :: shift_back = 5
    integer :: alphabet_size = 26

    read *, encoded
    
    do i = 1, len_trim(encoded)
        char_code = iachar(encoded(i:i))
        
        if (char_code >= ichar('a') .and. char_code <= ichar('z')) then
            char_code = char_code - shift_back
            if (char_code < ichar('a')) then
                char_code = char_code + alphabet_size
            end if
            decoded(i:i) = achar(char_code)
        else if (char_code >= ichar('A') .and. char_code <= ichar('Z')) then
            char_code = char_code - shift_back
            if (char_code < ichar('A')) then
                char_code = char_code + alphabet_size
            end if
            decoded(i:i) = achar(char_code)
        else
            decoded(i:i) = encoded(i:i)
        end if
    end do
    
    print *, trim(decoded)
end program decode_shift
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,33 @@
 program decode_shift
     implicit none
-    character(len=100) :: input_str
-    character(len=100) :: result
+    character(len=100) :: encoded
+    character(len=100) :: decoded
     integer :: i
     integer :: char_code
-    integer :: shifted_code
+    integer :: shift_back = 5
+    integer :: alphabet_size = 26
+
+    read *, encoded
     
-    read *, input_str
-    
-    result = input_str
-    
-    do i = 1, len_trim(input_str)
-        char_code = iachar(input_str(i:i))
+    do i = 1, len_trim(encoded)
+        char_code = iachar(encoded(i:i))
         
         if (char_code >= ichar('a') .and. char_code <= ichar('z')) then
-            shifted_code = char_code - 5
-            if (shifted_code < ichar('a')) then
-                shifted_code = shifted_code + 26
+            char_code = char_code - shift_back
+            if (char_code < ichar('a')) then
+                char_code = char_code + alphabet_size
             end if
-            result(i:i) = achar(shifted_code)
+            decoded(i:i) = achar(char_code)
         else if (char_code >= ichar('A') .and. char_code <= ichar('Z')) then
-            shifted_code = char_code - 5
-            if (shifted_code < ichar('A')) then
-                shifted_code = shifted_code + 26
+            char_code = char_code - shift_back
+            if (char_code < ichar('A')) then
+                char_code = char_code + alphabet_size
             end if
-            result(i:i) = achar(shifted_code)
+            decoded(i:i) = achar(char_code)
+        else
+            decoded(i:i) = encoded(i:i)
         end if
     end do
     
-    print *, result
+    print *, trim(decoded)
 end program decode_shift
```
