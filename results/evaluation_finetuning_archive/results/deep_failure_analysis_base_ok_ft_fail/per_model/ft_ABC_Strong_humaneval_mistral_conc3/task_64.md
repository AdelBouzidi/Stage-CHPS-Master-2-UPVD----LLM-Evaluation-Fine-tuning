# Failure case: ft_ABC_Strong_humaneval_mistral_conc3 / task 64

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


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
    "ft": 30
  },
  "num_nonempty_lines": {
    "base": 23,
    "ft": 25
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
  character(len=*) :: input_str
  integer :: result

  read *, input_str
  result = vowels_count(input_str)
  print *, result

contains

  function vowels_count(s) result(count)
    implicit none
    character(len=*), intent(in) :: s
    integer :: count
    integer :: i
    character(len=1) :: c

    count = 0
    do i = 1, len_trim(s)
      c = s(i:i)
      if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
          c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U' .or. &
          (c == 'y' .or. c == 'Y' .and. i == len_trim(s))) then
        count = count + 1
      end if
    end do
  end function vowels_count

end program vowels_count_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,30 @@
-program count_vowels
+program vowels_count_demo
+  implicit none
+  character(len=*) :: input_str
+  integer :: result
+
+  read *, input_str
+  result = vowels_count(input_str)
+  print *, result
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
+    character(len=1) :: c
 
-    read *, s
     count = 0
-    len_s = len_trim(s)
+    do i = 1, len_trim(s)
+      c = s(i:i)
+      if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
+          c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U' .or. &
+          (c == 'y' .or. c == 'Y' .and. i == len_trim(s))) then
+        count = count + 1
+      end if
+    end do
+  end function vowels_count
 
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
