# Failure case: ft_AC_antineighbor_humaneval_mistral_conc20 / task 64

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `status_ok`


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
{}
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
program vowels_count
  implicit none
  character(len=100) :: s
  integer :: count
  integer :: i
  character(len=1) :: ch

  read *, s
  count = 0
  do i = 1, len_trim(s)
    ch = s(i:i)
    select case (ichar(ch))
    case (ichar('a'), ichar('e'), ichar('i'), ichar('o'), ichar('u'))
      count = count + 1
    case (ichar('A'), ichar('E'), ichar('I'), ichar('O'), ichar('U'))
      count = count + 1
    case (ichar('y'), ichar('Y'))
      if (i == len_trim(s)) then
        count = count + 1
      end if
    end select
  end do

  print *, count

end program vowels_count
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,26 @@
-program count_vowels
-    implicit none
-    character(len=256) :: s
-    integer :: count
-    integer :: i
-    character :: c
-    integer :: len_s
+program vowels_count
+  implicit none
+  character(len=100) :: s
+  integer :: count
+  integer :: i
+  character(len=1) :: ch
 
-    read *, s
-    count = 0
-    len_s = len_trim(s)
+  read *, s
+  count = 0
+  do i = 1, len_trim(s)
+    ch = s(i:i)
+    select case (ichar(ch))
+    case (ichar('a'), ichar('e'), ichar('i'), ichar('o'), ichar('u'))
+      count = count + 1
+    case (ichar('A'), ichar('E'), ichar('I'), ichar('O'), ichar('U'))
+      count = count + 1
+    case (ichar('y'), ichar('Y'))
+      if (i == len_trim(s)) then
+        count = count + 1
+      end if
+    end select
+  end do
 
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
+  print *, count
 
-    print *, count
-end program count_vowels
+end program vowels_count
```
