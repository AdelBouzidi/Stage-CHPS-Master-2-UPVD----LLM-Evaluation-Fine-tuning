# Failure case: ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 61

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


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
    "base": 35,
    "ft": 24
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 24
  },
  "uses_read_stdin": {
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
program correct_bracketing
  implicit none
  character(len=100) :: brackets
  logical :: result
  read *, brackets
  result = correct_bracketing(brackets)
  print *, result
contains
  function correct_bracketing(brackets) result(res)
    implicit none
    character(len=*), intent(in) :: brackets
    logical :: res
    integer :: i, open_count
    open_count = 0
    do i = 1, len(brackets)
      if (brackets(i:i) == '(') then
        open_count = open_count + 1
      else if (brackets(i:i) == ')') then
        open_count = open_count - 1
      end if
    end do
    res = (open_count == 0)
  end function correct_bracketing
end program correct_bracketing
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,35 +1,24 @@
-program check_brackets
+program correct_bracketing
+  implicit none
+  character(len=100) :: brackets
+  logical :: result
+  read *, brackets
+  result = correct_bracketing(brackets)
+  print *, result
+contains
+  function correct_bracketing(brackets) result(res)
     implicit none
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
+    character(len=*), intent(in) :: brackets
+    logical :: res
+    integer :: i, open_count
+    open_count = 0
+    do i = 1, len(brackets)
+      if (brackets(i:i) == '(') then
+        open_count = open_count + 1
+      else if (brackets(i:i) == ')') then
+        open_count = open_count - 1
+      end if
     end do
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
+    res = (open_count == 0)
+  end function correct_bracketing
+end program correct_bracketing
```
