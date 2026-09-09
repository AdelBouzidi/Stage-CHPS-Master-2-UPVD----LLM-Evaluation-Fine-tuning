# Failure case: ft_ABC_source_stack_v1_humaneval_mistral_conc20 / task 50

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `static_modifies_intent_in_possible, status_ok`


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
    "ft": 38
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 30
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

  ! Read input
  read *, s

  ! Call decode_shift function
  result = decode_shift(s)

  ! Print output
  print *, result

contains

  function decode_shift(s)
    implicit none
    character(len=*), intent(in) :: s
    character(len=len(s)) :: decode_shift
    integer :: i
    character :: c

    do i = 1, len(s)
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        decode_shift(i:i) = char(ichar(c) - 5)
      else if (c >= 'A' .and. c <= 'Z') then
        decode_shift(i:i) = char(ichar(c) - 5)
      else
        decode_shift(i:i) = c
      end if
    end do

  end function decode_shift

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,38 @@
-program decode_shift
+program main
+  implicit none
+  character(len=100) :: s
+  character(len=100) :: result
+  integer :: i
+
+  ! Read input
+  read *, s
+
+  ! Call decode_shift function
+  result = decode_shift(s)
+
+  ! Print output
+  print *, result
+
+contains
+
+  function decode_shift(s)
     implicit none
-    character(len=100) :: input_str
-    character(len=100) :: result
+    character(len=*), intent(in) :: s
+    character(len=len(s)) :: decode_shift
     integer :: i
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
+    character :: c
+
+    do i = 1, len(s)
+      c = s(i:i)
+      if (c >= 'a' .and. c <= 'z') then
+        decode_shift(i:i) = char(ichar(c) - 5)
+      else if (c >= 'A' .and. c <= 'Z') then
+        decode_shift(i:i) = char(ichar(c) - 5)
+      else
+        decode_shift(i:i) = c
+      end if
     end do
-    
-    print *, result
-end program decode_shift
+
+  end function decode_shift
+
+end program main
```
