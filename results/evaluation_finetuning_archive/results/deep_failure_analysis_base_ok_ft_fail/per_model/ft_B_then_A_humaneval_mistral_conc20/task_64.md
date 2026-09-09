# Failure case: ft_B_then_A_humaneval_mistral_conc20 / task 64

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_compile_err`


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
  "has_debug_words": {
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 26,
    "ft": 25
  },
  "num_nonempty_lines": {
    "base": 23,
    "ft": 21
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
          character(len=*) :: input_string
          integer :: count
          integer :: i
          character(len=1) :: char

          read(*, '(A)') input_string

          count = 0
          do i = 1, len(input_string)
            char = input_string(i:i)
            select case (lowercase(char))
            case ('a', 'e', 'i', 'o', 'u')
              count = count + 1
            case ('y')
              if (i == len(input_string)) then
                count = count + 1
              end if
            end select
          end do

          print *, count

        end program vowels_count_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,25 @@
-program count_vowels
-    implicit none
-    character(len=256) :: s
-    integer :: count
-    integer :: i
-    character :: c
-    integer :: len_s
+program vowels_count_demo
+          implicit none
+          character(len=*) :: input_string
+          integer :: count
+          integer :: i
+          character(len=1) :: char
 
-    read *, s
-    count = 0
-    len_s = len_trim(s)
+          read(*, '(A)') input_string
 
-    do i = 1, len_s
-        c = s(i:i)
-        if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
-            c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U') then
-            count = count + 1
-        else if (c == 'y' .or. c == 'Y') then
-            if (i == len_s) then
+          count = 0
+          do i = 1, len(input_string)
+            char = input_string(i:i)
+            select case (lowercase(char))
+            case ('a', 'e', 'i', 'o', 'u')
+              count = count + 1
+            case ('y')
+              if (i == len(input_string)) then
                 count = count + 1
-            end if
-        end if
-    end do
+              end if
+            end select
+          end do
 
-    print *, count
-end program count_vowels
+          print *, count
+
+        end program vowels_count_demo
```
