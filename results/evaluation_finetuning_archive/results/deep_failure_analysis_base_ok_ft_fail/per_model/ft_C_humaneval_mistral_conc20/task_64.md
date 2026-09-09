# Failure case: ft_C_humaneval_mistral_conc20 / task 64

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
    "ft": 24
  },
  "num_nonempty_lines": {
    "base": 23,
    "ft": 21
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
    character(len=*) :: s
    integer :: count, i, len_s
    character :: c
    
    read *, s
    count = 0
    len_s = len_trim(s)
    
    do i = 1, len_s
        c = trim(s(i:i))
        select case (c)
        case ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
            count = count + 1
        case ('y', 'Y')
            if (i == len_s) then
                count = count + 1
            end if
        end select
    end do
    
    print *, count
end program vowel_counter
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,24 @@
-program count_vowels
+program vowel_counter
     implicit none
-    character(len=256) :: s
-    integer :: count
-    integer :: i
+    character(len=*) :: s
+    integer :: count, i, len_s
     character :: c
-    integer :: len_s
-
+    
     read *, s
     count = 0
     len_s = len_trim(s)
-
+    
     do i = 1, len_s
-        c = s(i:i)
-        if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
-            c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U') then
+        c = trim(s(i:i))
+        select case (c)
+        case ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
             count = count + 1
-        else if (c == 'y' .or. c == 'Y') then
+        case ('y', 'Y')
             if (i == len_s) then
                 count = count + 1
             end if
-        end if
+        end select
     end do
-
+    
     print *, count
-end program count_vowels
+end program vowel_counter
```
