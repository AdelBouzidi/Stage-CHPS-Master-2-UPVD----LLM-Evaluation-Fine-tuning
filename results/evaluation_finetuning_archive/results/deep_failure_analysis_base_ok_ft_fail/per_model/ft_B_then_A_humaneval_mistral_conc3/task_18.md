# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 18

- Base status: `ok`

- FT status: `runtime_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_runtime_err`


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
  "uses_allocatable": {
    "base": false,
    "ft": true
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
      character(len=:), allocatable :: string, substring
      integer :: count, pos, len_str, len_sub

      ! Read input
      read(*, *) string
      read(*, *) substring

      ! Initialize
      count = 0
      len_str = len(string)
      len_sub = len(substring)

      ! Count occurrences
      pos = 1
      do while (pos <= len_str - len_sub + 1)
        if (string(pos:pos+len_sub-1) == substring) then
          count = count + 1
        end if
        pos = pos + 1
      end do

      ! Output
      print *, count
    end program how_many_times_demo
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
-    count = 0
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
+program how_many_times_demo
+      implicit none
+      character(len=:), allocatable :: string, substring
+      integer :: count, pos, len_str, len_sub
+
+      ! Read input
+      read(*, *) string
+      read(*, *) substring
+
+      ! Initialize
+      count = 0
+      len_str = len(string)
+      len_sub = len(substring)
+
+      ! Count occurrences
+      pos = 1
+      do while (pos <= len_str - len_sub + 1)
+        if (string(pos:pos+len_sub-1) == substring) then
+          count = count + 1
+        end if
+        pos = pos + 1
+      end do
+
+      ! Output
+      print *, count
+    end program how_many_times_demo
```
