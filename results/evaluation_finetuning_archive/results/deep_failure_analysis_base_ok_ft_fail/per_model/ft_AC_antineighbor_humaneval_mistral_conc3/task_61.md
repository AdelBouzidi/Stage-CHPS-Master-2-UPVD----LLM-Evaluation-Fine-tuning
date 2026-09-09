# Failure case: ft_AC_antineighbor_humaneval_mistral_conc3 / task 61

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ineq`


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
    "ft": 31
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 25
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
program correct_bracketing
  implicit none
  character(len=100) :: brackets
  integer :: i, n
  logical :: result

  ! Read input from stdin
  read(*, '(A)') brackets

  ! Initialize result
  result = .true.

  ! Count opening and closing brackets
  n = 0
  do i = 1, len(brackets)
    if (brackets(i:i) == '(') then
      n = n + 1
    else if (brackets(i:i) == ')') then
      n = n - 1
    end if
  end do

  ! Check if brackets are correctly matched
  if (n /= 0) then
    result = .false.
  end if

  ! Output result
  print *, result

end program correct_bracketing
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,35 +1,31 @@
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
+program correct_bracketing
+  implicit none
+  character(len=100) :: brackets
+  integer :: i, n
+  logical :: result
+
+  ! Read input from stdin
+  read(*, '(A)') brackets
+
+  ! Initialize result
+  result = .true.
+
+  ! Count opening and closing brackets
+  n = 0
+  do i = 1, len(brackets)
+    if (brackets(i:i) == '(') then
+      n = n + 1
+    else if (brackets(i:i) == ')') then
+      n = n - 1
     end if
-    
-    ! Output result
-    print *, result
-    
-end program check_brackets
+  end do
+
+  ! Check if brackets are correctly matched
+  if (n /= 0) then
+    result = .false.
+  end if
+
+  ! Output result
+  print *, result
+
+end program correct_bracketing
```
