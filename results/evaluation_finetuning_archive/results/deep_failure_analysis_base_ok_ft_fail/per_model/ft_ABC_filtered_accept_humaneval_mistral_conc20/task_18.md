# Failure case: ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 18

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


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
  "has_contains": {
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
    "ft": 28
  },
  "num_nonempty_lines": {
    "base": 22,
    "ft": 28
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
program how_many_times_demo
  implicit none
  character(len=*) :: string, substring
  integer :: count
  read *, string
  read *, substring
  count = how_many_times(string, substring)
  print *, count
contains
  function how_many_times(string, substring) result(count)
    implicit none
    character(len=*), intent(in) :: string, substring
    integer :: count
    integer :: i, len_str, len_sub
    len_str = len_trim(string)
    len_sub = len_trim(substring)
    count = 0
    if (len_sub > len_str) then
      count = 0
    else
      do i = 1, len_str - len_sub + 1
        if (string(i:i+len_sub-1) == substring) then
          count = count + 1
        end if
      end do
    end if
  end function how_many_times
end program how_many_times_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,28 @@
-program count_substring
+program how_many_times_demo
+  implicit none
+  character(len=*) :: string, substring
+  integer :: count
+  read *, string
+  read *, substring
+  count = how_many_times(string, substring)
+  print *, count
+contains
+  function how_many_times(string, substring) result(count)
     implicit none
-    character(len=100) :: string, substring
-    integer :: count, i, len_str, len_sub
-    
-    ! Read input from stdin
-    read(*, '(A)') string
-    read(*, '(A)') substring
-    
-    ! Get lengths
+    character(len=*), intent(in) :: string, substring
+    integer :: count
+    integer :: i, len_str, len_sub
     len_str = len_trim(string)
     len_sub = len_trim(substring)
-    
-    ! Count overlapping occurrences
     count = 0
-    if (len_sub > 0 .and. len_sub <= len_str) then
-        do i = 1, len_str - len_sub + 1
-            if (string(i:i+len_sub-1) == substring) then
-                count = count + 1
-            end if
-        end do
+    if (len_sub > len_str) then
+      count = 0
+    else
+      do i = 1, len_str - len_sub + 1
+        if (string(i:i+len_sub-1) == substring) then
+          count = count + 1
+        end if
+      end do
     end if
-    
-    ! Output result to stdout
-    write(*, '(I0)') count
-end program count_substring
+  end function how_many_times
+end program how_many_times_demo
```
