# Failure case: ft_ABC_source_stack_v1_humaneval_mistral_conc20 / task 64

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ineq`


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
    "ft": 32
  },
  "num_nonempty_lines": {
    "base": 23,
    "ft": 27
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
program main
  implicit none
  character(len=100) :: s
  integer :: count
  integer :: i
  character(len=1) :: c

  ! Read input string
  read(*, '(A)') s

  ! Initialize count
  count = 0

  ! Loop through each character
  do i = 1, len(s)
    c = s(i:i)
    ! Check if character is a vowel (case insensitive)
    if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
        c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U') then
      count = count + 1
    else if (c == 'y' .or. c == 'Y') then
      ! 'y' is a vowel only at the end of the word
      if (i == len(s)) then
        count = count + 1
      end if
    end if
  end do

  ! Output the count
  print *, count

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,32 @@
-program count_vowels
-    implicit none
-    character(len=256) :: s
-    integer :: count
-    integer :: i
-    character :: c
-    integer :: len_s
+program main
+  implicit none
+  character(len=100) :: s
+  integer :: count
+  integer :: i
+  character(len=1) :: c
 
-    read *, s
-    count = 0
-    len_s = len_trim(s)
+  ! Read input string
+  read(*, '(A)') s
 
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
+  ! Initialize count
+  count = 0
 
-    print *, count
-end program count_vowels
+  ! Loop through each character
+  do i = 1, len(s)
+    c = s(i:i)
+    ! Check if character is a vowel (case insensitive)
+    if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
+        c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U') then
+      count = count + 1
+    else if (c == 'y' .or. c == 'Y') then
+      ! 'y' is a vowel only at the end of the word
+      if (i == len(s)) then
+        count = count + 1
+      end if
+    end if
+  end do
+
+  ! Output the count
+  print *, count
+
+end program main
```
