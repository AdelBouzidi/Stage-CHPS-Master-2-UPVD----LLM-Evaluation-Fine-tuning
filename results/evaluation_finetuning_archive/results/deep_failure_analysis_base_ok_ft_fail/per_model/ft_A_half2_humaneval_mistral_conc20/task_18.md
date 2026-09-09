# Failure case: ft_A_half2_humaneval_mistral_conc20 / task 18

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ok`


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
    "ft": 43
  },
  "num_nonempty_lines": {
    "base": 22,
    "ft": 35
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
program how_many_times_demo
  implicit none
  character(len=100) :: string
  character(len=100) :: substring
  integer :: result

  ! Read input
  read(*, '(a)') string
  read(*, '(a)') substring

  ! Call the function
  result = how_many_times(string, substring)

  ! Output result
  print *, result

contains

  function how_many_times(string, substring) result(res)
    implicit none
    character(len=*), intent(in) :: string
    character(len=*), intent(in) :: substring
    integer :: res
    integer :: i, len_str, len_sub
    character(len=len(string)) :: str
    character(len=len(substring)) :: sub

    len_str = len_trim(string)
    len_sub = len_trim(substring)
    
    if (len_sub > len_str) then
      res = 0
    else
      res = 0
      do i = 1, len_str - len_sub + 1
        if (string(i:i+len_sub-1) == substring(1:len_sub)) then
          res = res + 1
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
@@ -1,26 +1,43 @@
-program count_substring
+program how_many_times_demo
+  implicit none
+  character(len=100) :: string
+  character(len=100) :: substring
+  integer :: result
+
+  ! Read input
+  read(*, '(a)') string
+  read(*, '(a)') substring
+
+  ! Call the function
+  result = how_many_times(string, substring)
+
+  ! Output result
+  print *, result
+
+contains
+
+  function how_many_times(string, substring) result(res)
     implicit none
-    character(len=100) :: string, substring
-    integer :: count, i, len_str, len_sub
-    
-    ! Read input from stdin
-    read(*, '(A)') string
-    read(*, '(A)') substring
-    
-    ! Get lengths
+    character(len=*), intent(in) :: string
+    character(len=*), intent(in) :: substring
+    integer :: res
+    integer :: i, len_str, len_sub
+    character(len=len(string)) :: str
+    character(len=len(substring)) :: sub
+
     len_str = len_trim(string)
     len_sub = len_trim(substring)
     
-    ! Count overlapping occurrences
-    count = 0
-    if (len_sub > 0 .and. len_sub <= len_str) then
-        do i = 1, len_str - len_sub + 1
-            if (string(i:i+len_sub-1) == substring) then
-                count = count + 1
-            end if
-        end do
+    if (len_sub > len_str) then
+      res = 0
+    else
+      res = 0
+      do i = 1, len_str - len_sub + 1
+        if (string(i:i+len_sub-1) == substring(1:len_sub)) then
+          res = res + 1
+        end if
+      end do
     end if
-    
-    ! Output result to stdout
-    write(*, '(I0)') count
-end program count_substring
+  end function how_many_times
+
+end program how_many_times_demo
```
