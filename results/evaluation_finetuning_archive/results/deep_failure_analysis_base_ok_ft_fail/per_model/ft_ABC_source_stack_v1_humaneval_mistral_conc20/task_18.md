# Failure case: ft_ABC_source_stack_v1_humaneval_mistral_conc20 / task 18

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `status_ok`


## Prompt

```text
Write a Fortran90 program that finds how many times a given substring can be found in the original string, counting overlapping occurrences.
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
    "base": true,
    "ft": false
  },
  "uses_print_star": {
    "base": false,
    "ft": true
  },
  "uses_read_stdin": {
    "base": true,
    "ft": false
  },
  "uses_write_star": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program count_substring
    implicit none
    character(len=100) :: string, substring
    integer :: count, i, len_str, len_sub
    
    ! Read input from stdin
    read(*, '(A)') string
    read(*, '(A)') substring
    
    ! Get lengths
    len_str = len_trim(string)
    len_sub = len_trim(substring)
    
    ! Count overlapping occurrences
    count = 0
    if (len_sub > 0 .and. len_sub <= len_str) then
        do i = 1, len_str - len_sub + 1
            if (string(i:i+len_sub-1) == substring) then
                count = count + 1
            end if
        end do
    end if
    
    ! Output result to stdout
    write(*, '(I0)') count
end program count_substring
```


## FT generated code

```fortran
program main
  implicit none
  character(len=100) :: string
  character(len=100) :: substring
  integer :: count
  integer :: i, j, len_str, len_sub

  read *, string
  read *, substring

  count = 0
  len_str = len_trim(string)
  len_sub = len_trim(substring)

  if (len_sub > len_str) then
    count = 0
  else
    do i = 1, len_str - len_sub + 1
      if (string(i:i+len_sub-1) == substring) then
        count = count + 1
      end if
    end do
  end if

  print *, count
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,26 @@
-program count_substring
-    implicit none
-    character(len=100) :: string, substring
-    integer :: count, i, len_str, len_sub
-    
-    ! Read input from stdin
-    read(*, '(A)') string
-    read(*, '(A)') substring
-    
-    ! Get lengths
-    len_str = len_trim(string)
-    len_sub = len_trim(substring)
-    
-    ! Count overlapping occurrences
+program main
+  implicit none
+  character(len=100) :: string
+  character(len=100) :: substring
+  integer :: count
+  integer :: i, j, len_str, len_sub
+
+  read *, string
+  read *, substring
+
+  count = 0
+  len_str = len_trim(string)
+  len_sub = len_trim(substring)
+
+  if (len_sub > len_str) then
     count = 0
-    if (len_sub > 0 .and. len_sub <= len_str) then
-        do i = 1, len_str - len_sub + 1
-            if (string(i:i+len_sub-1) == substring) then
-                count = count + 1
-            end if
-        end do
-    end if
-    
-    ! Output result to stdout
-    write(*, '(I0)') count
-end program count_substring
+  else
+    do i = 1, len_str - len_sub + 1
+      if (string(i:i+len_sub-1) == substring) then
+        count = count + 1
+      end if
+    end do
+  end if
+
+  print *, count
+end program main
```
