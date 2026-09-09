# Failure case: ft_ABC_source_numericalhub_humaneval_mistral_conc20 / task 64

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


## Prompt

```text
Write a Fortran90 program that counts the number of vowels in a string. Vowels are 'a', 'e', 'i', 'o', 'u' (case insensitive) and 'y' is considered a vowel only when it is at the end of the word.
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
  "has_debug_words": {
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
    "base": 26,
    "ft": 38
  },
  "num_nonempty_lines": {
    "base": 23,
    "ft": 31
  },
  "uses_read_stdin": {
    "base": false,
    "ft": true
  }
}
```


## Base generated code

```fortran
program count_vowels
    implicit none
    character(len=256) :: s
    integer :: count
    integer :: i
    character :: c
    integer :: len_s

    read *, s
    count = 0
    len_s = len_trim(s)

    do i = 1, len_s
        c = s(i:i)
        if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
            c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U') then
            count = count + 1
        else if (c == 'y' .or. c == 'Y') then
            if (i == len_s) then
                count = count + 1
            end if
        end if
    end do

    print *, count
end program count_vowels
```


## FT generated code

```fortran
program vowels_count_demo
  implicit none
  integer :: count
  character(len=100) :: input_str
  
  ! Read input from stdin
  read(*, '(t)(a)') input_str
  
  ! Call the function
  count = vowels_count(input_str)
  
  ! Print result
  print *, count
  
contains

  function vowels_count(s) result(count)
    implicit none
    character(len=*), intent(in) :: s
    integer :: count
    integer :: i
    character(len=1) :: ch
    
    count = 0
    do i = 1, len_trim(s)
      ch = s(i:i)
      if (ch == 'a' .or. ch == 'e' .or. ch == 'i' .or. ch == 'o' .or. ch == 'u' .or. &
          ch == 'A' .or. ch == 'E' .or. ch == 'I' .or. ch == 'O' .or. ch == 'U') then
        count = count + 1
      else if (ch == 'y' .or. ch == 'Y') then
        if (i == len_trim(s)) then
          count = count + 1
        end if
      end if
    end do
  end function vowels_count

end program vowels_count_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,38 @@
-program count_vowels
+program vowels_count_demo
+  implicit none
+  integer :: count
+  character(len=100) :: input_str
+  
+  ! Read input from stdin
+  read(*, '(t)(a)') input_str
+  
+  ! Call the function
+  count = vowels_count(input_str)
+  
+  ! Print result
+  print *, count
+  
+contains
+
+  function vowels_count(s) result(count)
     implicit none
-    character(len=256) :: s
+    character(len=*), intent(in) :: s
     integer :: count
     integer :: i
-    character :: c
-    integer :: len_s
+    character(len=1) :: ch
+    
+    count = 0
+    do i = 1, len_trim(s)
+      ch = s(i:i)
+      if (ch == 'a' .or. ch == 'e' .or. ch == 'i' .or. ch == 'o' .or. ch == 'u' .or. &
+          ch == 'A' .or. ch == 'E' .or. ch == 'I' .or. ch == 'O' .or. ch == 'U') then
+        count = count + 1
+      else if (ch == 'y' .or. ch == 'Y') then
+        if (i == len_trim(s)) then
+          count = count + 1
+        end if
+      end if
+    end do
+  end function vowels_count
 
-    read *, s
-    count = 0
-    len_s = len_trim(s)
-
-    do i = 1, len_s
-        c = s(i:i)
-        if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
-            c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U') then
-            count = count + 1
-        else if (c == 'y' .or. c == 'Y') then
-            if (i == len_s) then
-                count = count + 1
-            end if
-        end if
-    end do
-
-    print *, count
-end program count_vowels
+end program vowels_count_demo
```
