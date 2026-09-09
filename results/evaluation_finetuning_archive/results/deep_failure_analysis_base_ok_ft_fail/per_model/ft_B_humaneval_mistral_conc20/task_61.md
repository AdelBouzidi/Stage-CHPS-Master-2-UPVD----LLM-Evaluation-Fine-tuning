# Failure case: ft_B_humaneval_mistral_conc20 / task 61

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `status_ineq`

- Labels: `status_ineq`


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
  "has_debug_words": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 35,
    "ft": 26
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 21
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
program check_brackets
  implicit none
  character(len=100) :: input
  integer :: i, count
  character(len=1) :: c
  
  read *, input
  
  count = 0
  
  do i = 1, len_trim(input)
    c = input(i:i)
    if (c == '(') then
      count = count + 1
    else if (c == ')') then
      count = count - 1
    end if
  end do
  
  if (count == 0) then
    print *, .true.
  else
    print *, .false.
  end if
  
end program check_brackets
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,35 +1,26 @@
 program check_brackets
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
+  implicit none
+  character(len=100) :: input
+  integer :: i, count
+  character(len=1) :: c
+  
+  read *, input
+  
+  count = 0
+  
+  do i = 1, len_trim(input)
+    c = input(i:i)
+    if (c == '(') then
+      count = count + 1
+    else if (c == ')') then
+      count = count - 1
     end if
-    
-    ! Output result
-    print *, result
-    
+  end do
+  
+  if (count == 0) then
+    print *, .true.
+  else
+    print *, .false.
+  end if
+  
 end program check_brackets
```
