# Failure case: ft_AB_shuffle_humaneval_mistral_conc3 / task 61

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_compile_err`


## Prompt

```text
Write a Fortran90 program that checks if every opening bracket in a given string of ( and ) has a corresponding closing bracket.
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
    "base": 35,
    "ft": 14
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 11
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program check_brackets
    implicit none
    character(len=100) :: input
    integer :: i, count
    logical :: result
    
    ! Read input from stdin
    read(*, '(A)') input
    
    ! Initialize counter
    count = 0
    result = .true.
    
    ! Check each character
    do i = 1, len_trim(input)
        if (input(i:i) == '(') then
            count = count + 1
        else if (input(i:i) == ')') then
            count = count - 1
            if (count < 0) then
                result = .false.
                exit
            end if
        end if
    end do
    
    ! Check if all brackets are matched
    if (count /= 0) then
        result = .false.
    end if
    
    ! Output result
    print *, result
    
end program check_brackets
```


## FT generated code

```fortran
program main
  implicit none
  character(len=100) :: brackets
  logical :: result

  ! Read input from stdin
  read(*, '(a)') brackets

  ! Call the function
  result = correct_bracketing(brackets)

  ! Output the result
  print *, result
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,35 +1,14 @@
-program check_brackets
-    implicit none
-    character(len=100) :: input
-    integer :: i, count
-    logical :: result
-    
-    ! Read input from stdin
-    read(*, '(A)') input
-    
-    ! Initialize counter
-    count = 0
-    result = .true.
-    
-    ! Check each character
-    do i = 1, len_trim(input)
-        if (input(i:i) == '(') then
-            count = count + 1
-        else if (input(i:i) == ')') then
-            count = count - 1
-            if (count < 0) then
-                result = .false.
-                exit
-            end if
-        end if
-    end do
-    
-    ! Check if all brackets are matched
-    if (count /= 0) then
-        result = .false.
-    end if
-    
-    ! Output result
-    print *, result
-    
-end program check_brackets
+program main
+  implicit none
+  character(len=100) :: brackets
+  logical :: result
+
+  ! Read input from stdin
+  read(*, '(a)') brackets
+
+  ! Call the function
+  result = correct_bracketing(brackets)
+
+  ! Output the result
+  print *, result
+end program main
```
