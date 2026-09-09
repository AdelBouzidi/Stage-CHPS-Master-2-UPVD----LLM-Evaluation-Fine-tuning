# Failure case: ft_AB_shuffle_humaneval_mistral_conc20 / task 61

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ok`


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
    "ft": 39
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 32
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

contains

  logical function correct_bracketing(brackets)
    implicit none
    character(len=*), intent(in) :: brackets
    integer :: i, open_count
    character(len=1) :: char

    open_count = 0
    do i = 1, len(brackets)
      char = brackets(i:i)
      if (char == '(') then
        open_count = open_count + 1
      else if (char == ')') then
        open_count = open_count - 1
        if (open_count < 0) then
          correct_bracketing = .false.
          return
        end if
      end if
    end do
    correct_bracketing = (open_count == 0)
  end function correct_bracketing

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,35 +1,39 @@
-program check_brackets
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
+
+contains
+
+  logical function correct_bracketing(brackets)
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
+    character(len=*), intent(in) :: brackets
+    integer :: i, open_count
+    character(len=1) :: char
+
+    open_count = 0
+    do i = 1, len(brackets)
+      char = brackets(i:i)
+      if (char == '(') then
+        open_count = open_count + 1
+      else if (char == ')') then
+        open_count = open_count - 1
+        if (open_count < 0) then
+          correct_bracketing = .false.
+          return
         end if
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
+    correct_bracketing = (open_count == 0)
+  end function correct_bracketing
+
+end program main
```
