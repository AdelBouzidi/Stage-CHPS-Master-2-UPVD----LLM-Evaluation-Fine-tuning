# Failure case: ft_C_then_A_humaneval_mistral_conc20 / task 50

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_output_labels`

- Labels: `static_modifies_intent_in_possible, static_output_labels, status_compile_err`


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
  "has_labels_in_output": {
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
    "ft": 45
  },
  "num_nonempty_lines": {
    "base": 27,
    "ft": 38
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
  character(len=*), parameter :: input_str = 'fgh'
  character(len=:), allocatable :: decoded
  integer :: i

  ! Call the decode_shift function
  decoded = decode_shift(input_str)

  ! Output the result
  print *, 'Decoded string:', decoded

contains

  function decode_shift(s) result(res)
    implicit none
    character(len=*), intent(in) :: s
    character(len=:), allocatable :: res
    integer :: i, len_s
    character(len=1) :: c

    len_s = len(s)
    allocate(character(len=len_s) :: res)

    do i = 1, len_s
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        if (c >= 'f') then
          res(i:i) = c - 5
        else
          res(i:i) = c + 21
        end if
      else if (c >= 'A' .and. c <= 'Z') then
        if (c >= 'F') then
          res(i:i) = c - 5
        else
          res(i:i) = c + 21
        end if
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
@@ -1,32 +1,45 @@
-program decode_shift
+program decode_shift_demo
+  implicit none
+  character(len=*), parameter :: input_str = 'fgh'
+  character(len=:), allocatable :: decoded
+  integer :: i
+
+  ! Call the decode_shift function
+  decoded = decode_shift(input_str)
+
+  ! Output the result
+  print *, 'Decoded string:', decoded
+
+contains
+
+  function decode_shift(s) result(res)
     implicit none
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
+    character(len=*), intent(in) :: s
+    character(len=:), allocatable :: res
+    integer :: i, len_s
+    character(len=1) :: c
+
+    len_s = len(s)
+    allocate(character(len=len_s) :: res)
+
+    do i = 1, len_s
+      c = s(i:i)
+      if (c >= 'a' .and. c <= 'z') then
+        if (c >= 'f') then
+          res(i:i) = c - 5
+        else
+          res(i:i) = c + 21
         end if
+      else if (c >= 'A' .and. c <= 'Z') then
+        if (c >= 'F') then
+          res(i:i) = c - 5
+        else
+          res(i:i) = c + 21
+        end if
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
