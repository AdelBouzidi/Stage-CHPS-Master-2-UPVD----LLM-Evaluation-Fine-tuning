# Failure case: ft_ABC_dedup_BC_humaneval_mistral_conc20 / task 18

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_output_labels`

- Labels: `static_modifies_intent_in_possible, static_output_labels, status_ineq`


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
  "has_labels_in_output": {
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
    "ft": 39
  },
  "num_nonempty_lines": {
    "base": 22,
    "ft": 30
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
  character(len=100) :: string, substring
  integer :: result

  ! Hardcoded input as per example
  string = 'aaa'
  substring = 'a'

  result = how_many_times(string, substring)
  print *, 'Result:', result

contains

  integer function how_many_times(string, substring)
    implicit none
    character(len=*), intent(in) :: string, substring
    integer :: i, count
    integer :: len_str, len_sub

    len_str = len_trim(string)
    len_sub = len_trim(substring)

    if (len_sub > len_str) then
      how_many_times = 0
      return
    end if

    count = 0
    do i = 1, len_str - len_sub + 1
      if (string(i:i+len_sub-1) == substring) then
        count = count + 1
      end if
    end do

    how_many_times = count
  end function how_many_times

end program how_many_times_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,39 @@
-program count_substring
+program how_many_times_demo
+  implicit none
+  character(len=100) :: string, substring
+  integer :: result
+
+  ! Hardcoded input as per example
+  string = 'aaa'
+  substring = 'a'
+
+  result = how_many_times(string, substring)
+  print *, 'Result:', result
+
+contains
+
+  integer function how_many_times(string, substring)
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
+    integer :: i, count
+    integer :: len_str, len_sub
+
     len_str = len_trim(string)
     len_sub = len_trim(substring)
-    
-    ! Count overlapping occurrences
+
+    if (len_sub > len_str) then
+      how_many_times = 0
+      return
+    end if
+
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
+    do i = 1, len_str - len_sub + 1
+      if (string(i:i+len_sub-1) == substring) then
+        count = count + 1
+      end if
+    end do
+
+    how_many_times = count
+  end function how_many_times
+
+end program how_many_times_demo
```
