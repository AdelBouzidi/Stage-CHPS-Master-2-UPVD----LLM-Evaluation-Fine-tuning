# Failure case: ft_C_humaneval_mistral_conc20 / task 18

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
  "has_debug_words": {
    "base": true,
    "ft": false
  },
  "modifies_intent_in_possible": {
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
program count_substring
    implicit none
    character(len=*), intent(in) :: string, substring
    integer :: count, i, len_str, len_sub
    
    ! Get input from stdin
    read(*, '(A)') string
    read(*, '(A)') substring
    
    ! Calculate lengths
    len_str = len_trim(string)
    len_sub = len_trim(substring)
    
    ! Count overlapping occurrences
    count = 0
    if (len_sub <= len_str) then
        do i = 1, len_str - len_sub + 1
            if (string(i:i+len_sub-1) == substring) then
                count = count + 1
            end if
        end do
    end if
    
    ! Output result
    print *, count
end program count_substring
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,19 +1,19 @@
 program count_substring
     implicit none
-    character(len=100) :: string, substring
+    character(len=*), intent(in) :: string, substring
     integer :: count, i, len_str, len_sub
     
-    ! Read input from stdin
+    ! Get input from stdin
     read(*, '(A)') string
     read(*, '(A)') substring
     
-    ! Get lengths
+    ! Calculate lengths
     len_str = len_trim(string)
     len_sub = len_trim(substring)
     
     ! Count overlapping occurrences
     count = 0
-    if (len_sub > 0 .and. len_sub <= len_str) then
+    if (len_sub <= len_str) then
         do i = 1, len_str - len_sub + 1
             if (string(i:i+len_sub-1) == substring) then
                 count = count + 1
@@ -21,6 +21,6 @@
         end do
     end if
     
-    ! Output result to stdout
-    write(*, '(I0)') count
+    ! Output result
+    print *, count
 end program count_substring
```
