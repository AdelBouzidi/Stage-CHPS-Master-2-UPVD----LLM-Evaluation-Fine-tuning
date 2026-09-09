# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 61

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
    "ft": 30
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 26
  },
  "uses_allocatable": {
    "base": false,
    "ft": true
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
program bracket_check
      implicit none
      character(len=*), allocatable :: brackets
      character(len=1) :: char
      integer :: i, balance
      logical :: result

      read(*, '(a)') brackets

      balance = 0
      result = .true.
      do i = 1, len(brackets)
         char = brackets(i:i)
         if (char == '(') then
            balance = balance + 1
         else if (char == ')') then
            balance = balance - 1
            if (balance < 0) then
               result = .false.
               exit
            end if
         end if
      end do
      if (balance /= 0) then
         result = .false.
      end if

      print *, result

    end program bracket_check
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,35 +1,30 @@
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
+program bracket_check
+      implicit none
+      character(len=*), allocatable :: brackets
+      character(len=1) :: char
+      integer :: i, balance
+      logical :: result
+
+      read(*, '(a)') brackets
+
+      balance = 0
+      result = .true.
+      do i = 1, len(brackets)
+         char = brackets(i:i)
+         if (char == '(') then
+            balance = balance + 1
+         else if (char == ')') then
+            balance = balance - 1
+            if (balance < 0) then
+               result = .false.
+               exit
             end if
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
+         end if
+      end do
+      if (balance /= 0) then
+         result = .false.
+      end if
+
+      print *, result
+
+    end program bracket_check
```
