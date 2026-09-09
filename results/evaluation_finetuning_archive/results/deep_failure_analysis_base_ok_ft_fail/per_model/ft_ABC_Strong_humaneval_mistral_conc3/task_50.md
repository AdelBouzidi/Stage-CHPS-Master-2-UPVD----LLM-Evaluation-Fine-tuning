# Failure case: ft_ABC_Strong_humaneval_mistral_conc3 / task 50

- Base status: `ok`

- FT status: `runtime_err`

- Primary cause: `status_runtime_err`

- Labels: `static_modifies_intent_in_possible, status_runtime_err`


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
    "ft": 31
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 26
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
  },
  "uses_allocatable": {
    "base": false,
    "ft": true
  },
  "uses_allocate": {
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
  character(len=:), allocatable :: input_str, result
  
  read *, input_str
  call decode_shift(input_str, result)
  print *, result
contains

  subroutine decode_shift(s, result)
    character(len=*), intent(in) :: s
    character(len=:), allocatable, intent(out) :: result
    integer :: i, n
    character(len=1) :: c
    
    n = len_trim(s)
    allocate(character(len=n) :: result)
    
    do i = 1, n
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        result(i:i) = char(ichar(c) - 5)
      else if (c >= 'A' .and. c <= 'Z') then
        result(i:i) = char(ichar(c) - 5)
      else
        result(i:i) = c
      end if
    end do
  end subroutine decode_shift

end program decode_shift_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,31 @@
-program decode_shift
-    implicit none
-    character(len=100) :: input_str
-    character(len=100) :: result
-    integer :: i
-    integer :: char_code
-    integer :: shifted_code
+program decode_shift_demo
+  implicit none
+  character(len=:), allocatable :: input_str, result
+  
+  read *, input_str
+  call decode_shift(input_str, result)
+  print *, result
+contains
+
+  subroutine decode_shift(s, result)
+    character(len=*), intent(in) :: s
+    character(len=:), allocatable, intent(out) :: result
+    integer :: i, n
+    character(len=1) :: c
     
-    read *, input_str
+    n = len_trim(s)
+    allocate(character(len=n) :: result)
     
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
+    do i = 1, n
+      c = s(i:i)
+      if (c >= 'a' .and. c <= 'z') then
+        result(i:i) = char(ichar(c) - 5)
+      else if (c >= 'A' .and. c <= 'Z') then
+        result(i:i) = char(ichar(c) - 5)
+      else
+        result(i:i) = c
+      end if
     end do
-    
-    print *, result
-end program decode_shift
+  end subroutine decode_shift
+
+end program decode_shift_demo
```
