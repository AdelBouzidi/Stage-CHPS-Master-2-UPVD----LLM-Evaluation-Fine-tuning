# Failure case: ft_B_humaneval_mistral_conc3 / task 64

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


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
  "num_lines": {
    "base": 26,
    "ft": 33
  },
  "num_nonempty_lines": {
    "base": 23,
    "ft": 28
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
program vowel_counter
    implicit none
    character(len=*) :: input
    integer :: count
    integer :: i
    character(len=1) :: ch
    logical :: is_vowel
    integer :: len_str

    read *, input
    len_str = len_trim(input)
    count = 0

    do i = 1, len_str
        ch = input(i:i)
        is_vowel = .false.
        if (ch == 'a' .or. ch == 'e' .or. ch == 'i' .or. ch == 'o' .or. ch == 'u' .or. &
            ch == 'A' .or. ch == 'E' .or. ch == 'I' .or. ch == 'O' .or. ch == 'U') then
            is_vowel = .true.
        else if (ch == 'y' .or. ch == 'Y') then
            if (i == len_str) then
                is_vowel = .true.
            end if
        end if

        if (is_vowel) then
            count = count + 1
        end if
    end do

    print *, count

end program vowel_counter
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,33 @@
-program count_vowels
+program vowel_counter
     implicit none
-    character(len=256) :: s
+    character(len=*) :: input
     integer :: count
     integer :: i
-    character :: c
-    integer :: len_s
+    character(len=1) :: ch
+    logical :: is_vowel
+    integer :: len_str
 
-    read *, s
+    read *, input
+    len_str = len_trim(input)
     count = 0
-    len_s = len_trim(s)
 
-    do i = 1, len_s
-        c = s(i:i)
-        if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
-            c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U') then
+    do i = 1, len_str
+        ch = input(i:i)
+        is_vowel = .false.
+        if (ch == 'a' .or. ch == 'e' .or. ch == 'i' .or. ch == 'o' .or. ch == 'u' .or. &
+            ch == 'A' .or. ch == 'E' .or. ch == 'I' .or. ch == 'O' .or. ch == 'U') then
+            is_vowel = .true.
+        else if (ch == 'y' .or. ch == 'Y') then
+            if (i == len_str) then
+                is_vowel = .true.
+            end if
+        end if
+
+        if (is_vowel) then
             count = count + 1
-        else if (c == 'y' .or. c == 'Y') then
-            if (i == len_s) then
-                count = count + 1
-            end if
         end if
     end do
 
     print *, count
-end program count_vowels
+
+end program vowel_counter
```
