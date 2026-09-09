# Failure case: ft_A_ep2_humaneval_mistral_conc20 / task 18

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


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
    "ft": 50
  },
  "num_nonempty_lines": {
    "base": 22,
    "ft": 40
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
program how_many_times
  implicit none
  character(len=*), dimension(2) :: input
  integer :: result

  ! Read input strings
  read(*, '(A)') input(1)
  read(*, '(A)') input(2)

  result = how_many_times(input(1), input(2))

  print *, result

contains

  integer function how_many_times(string, substring)
    character(len=*), intent(in) :: string
    character(len=*), intent(in) :: substring
    integer :: i, len_str, len_sub
    logical :: match

    len_str = len_trim(string)
    len_sub = len_trim(substring)

    if (len_sub == 0) then
      how_many_times = 0
      return
    end if

    if (len_sub > len_str) then
      how_many_times = 0
      return
    end if

    how_many_times = 0
    do i = 1, len_str - len_sub + 1
      match = .true.
      do j = 1, len_sub
        if (string(i+j-1:i+j-1) /= substring(1:1)) then
          match = .false.
          exit
        end if
      end do
      if (match) then
        how_many_times = how_many_times + 1
      end if
    end do
  end function how_many_times

end program how_many_times
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,26 +1,50 @@
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
+program how_many_times
+  implicit none
+  character(len=*), dimension(2) :: input
+  integer :: result
+
+  ! Read input strings
+  read(*, '(A)') input(1)
+  read(*, '(A)') input(2)
+
+  result = how_many_times(input(1), input(2))
+
+  print *, result
+
+contains
+
+  integer function how_many_times(string, substring)
+    character(len=*), intent(in) :: string
+    character(len=*), intent(in) :: substring
+    integer :: i, len_str, len_sub
+    logical :: match
+
     len_str = len_trim(string)
     len_sub = len_trim(substring)
-    
-    ! Count overlapping occurrences
-    count = 0
-    if (len_sub > 0 .and. len_sub <= len_str) then
-        do i = 1, len_str - len_sub + 1
-            if (string(i:i+len_sub-1) == substring) then
-                count = count + 1
-            end if
-        end do
+
+    if (len_sub == 0) then
+      how_many_times = 0
+      return
     end if
-    
-    ! Output result to stdout
-    write(*, '(I0)') count
-end program count_substring
+
+    if (len_sub > len_str) then
+      how_many_times = 0
+      return
+    end if
+
+    how_many_times = 0
+    do i = 1, len_str - len_sub + 1
+      match = .true.
+      do j = 1, len_sub
+        if (string(i+j-1:i+j-1) /= substring(1:1)) then
+          match = .false.
+          exit
+        end if
+      end do
+      if (match) then
+        how_many_times = how_many_times + 1
+      end if
+    end do
+  end function how_many_times
+
+end program how_many_times
```
