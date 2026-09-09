# Failure case: ft_ABC_dedup_BC_humaneval_mistral_conc20 / task 64

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
    "ft": 40
  },
  "num_nonempty_lines": {
    "base": 23,
    "ft": 31
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
program vowels_count
  implicit none
  character(len=100) :: input
  integer :: result

  ! Read input string
  read *, input

  ! Count vowels
  result = vowels_count(input)

  ! Output result
  print *, result

contains

  integer function vowels_count(s)
    character(len=*), intent(in) :: s
    integer :: i, len_s, count
    character(len=1) :: c

    len_s = len_trim(s)
    count = 0

    do i = 1, len_s
      c = s(i:i)
      select case (c)
      case ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
        count = count + 1
      case ('y', 'Y')
        if (i == len_s) then
          count = count + 1
        end if
      end select
    end do

    vowels_count = count
  end function vowels_count

end program vowels_count
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,40 @@
-program count_vowels
-    implicit none
-    character(len=256) :: s
-    integer :: count
-    integer :: i
-    character :: c
-    integer :: len_s
+program vowels_count
+  implicit none
+  character(len=100) :: input
+  integer :: result
 
-    read *, s
+  ! Read input string
+  read *, input
+
+  ! Count vowels
+  result = vowels_count(input)
+
+  ! Output result
+  print *, result
+
+contains
+
+  integer function vowels_count(s)
+    character(len=*), intent(in) :: s
+    integer :: i, len_s, count
+    character(len=1) :: c
+
+    len_s = len_trim(s)
     count = 0
-    len_s = len_trim(s)
 
     do i = 1, len_s
-        c = s(i:i)
-        if (c == 'a' .or. c == 'e' .or. c == 'i' .or. c == 'o' .or. c == 'u' .or. &
-            c == 'A' .or. c == 'E' .or. c == 'I' .or. c == 'O' .or. c == 'U') then
-            count = count + 1
-        else if (c == 'y' .or. c == 'Y') then
-            if (i == len_s) then
-                count = count + 1
-            end if
+      c = s(i:i)
+      select case (c)
+      case ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
+        count = count + 1
+      case ('y', 'Y')
+        if (i == len_s) then
+          count = count + 1
         end if
+      end select
     end do
 
-    print *, count
-end program count_vowels
+    vowels_count = count
+  end function vowels_count
+
+end program vowels_count
```
