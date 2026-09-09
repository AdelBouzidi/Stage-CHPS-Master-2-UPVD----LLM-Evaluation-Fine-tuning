# Failure case: ft_A_half1_humaneval_mistral_conc20 / task 50

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


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
  "num_lines": {
    "base": 32,
    "ft": 23
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 18
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
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
  character(len=*) :: input
  character(len=*) :: result

  read *, input
  call decode_shift(input, result)
  print *, result

contains

  subroutine decode_shift(s, result)
    character(len=*), intent(in) :: s
    character(len=*), intent(out) :: result
    integer :: i, len_s

    len_s = len(s)
    do i = 1, len_s
      result(i:i) = char(ichar(s(i:i)) - 5)
    end do
  end subroutine decode_shift

end program decode_shift_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,23 @@
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
+program decode_shift_demo
+  implicit none
+  character(len=*) :: input
+  character(len=*) :: result
+
+  read *, input
+  call decode_shift(input, result)
+  print *, result
+
+contains
+
+  subroutine decode_shift(s, result)
+    character(len=*), intent(in) :: s
+    character(len=*), intent(out) :: result
+    integer :: i, len_s
+
+    len_s = len(s)
+    do i = 1, len_s
+      result(i:i) = char(ichar(s(i:i)) - 5)
     end do
-    
-    print *, result
-end program decode_shift
+  end subroutine decode_shift
+
+end program decode_shift_demo
```
