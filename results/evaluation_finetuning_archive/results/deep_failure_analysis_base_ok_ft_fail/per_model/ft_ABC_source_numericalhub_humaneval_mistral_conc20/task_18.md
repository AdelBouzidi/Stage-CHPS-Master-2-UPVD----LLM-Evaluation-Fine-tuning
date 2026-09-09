# Failure case: ft_ABC_source_numericalhub_humaneval_mistral_conc20 / task 18

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ineq`


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
    "ft": 30
  },
  "num_nonempty_lines": {
    "base": 22,
    "ft": 25
  },
  "uses_print_star": {
    "base": false,
    "ft": true
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
program test_how_many_times
  implicit none
  integer, parameter :: i4b = selected_int_kind(9)
  character(len=100) :: string, substring
  integer :: result

  ! Read input from stdin
  read(*,*) string, substring
  result = how_many_times(string, substring)
  print *, result

contains

  integer function how_many_times(string, substring)
    character(len=*), intent(in) :: string, substring
    integer :: i, n, m, count
    character(len=len(string)) :: temp

    n = len(string)
    m = len(substring)
    count = 0
    do i = 1, n - m + 1
      if (string(i:i+m-1) == substring) then
        count = count + 1
      end if
    end do
    how_many_times = count
  end function how_many_times

end program test_how_many_times
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,30 @@
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
+program test_how_many_times
+  implicit none
+  integer, parameter :: i4b = selected_int_kind(9)
+  character(len=100) :: string, substring
+  integer :: result
+
+  ! Read input from stdin
+  read(*,*) string, substring
+  result = how_many_times(string, substring)
+  print *, result
+
+contains
+
+  integer function how_many_times(string, substring)
+    character(len=*), intent(in) :: string, substring
+    integer :: i, n, m, count
+    character(len=len(string)) :: temp
+
+    n = len(string)
+    m = len(substring)
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
+    do i = 1, n - m + 1
+      if (string(i:i+m-1) == substring) then
+        count = count + 1
+      end if
+    end do
+    how_many_times = count
+  end function how_many_times
+
+end program test_how_many_times
```
