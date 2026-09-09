# Failure case: ft_AB_antineighbor_humaneval_mistral_conc20 / task 61

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
  "num_lines": {
    "base": 35,
    "ft": 24
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 18
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
  character(len=100) :: input_str
  integer :: i, count_open, count_close
  logical :: result

  read *, input_str

  count_open = 0
  count_close = 0

  do i = 1, len_trim(input_str)
    if (input_str(i:i) == '(') then
      count_open = count_open + 1
    else if (input_str(i:i) == ')') then
      count_close = count_close + 1
    end if
  end do

  result = (count_open == count_close)

  print *, result

end program correct_bracketing
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,35 +1,24 @@
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
+  character(len=100) :: input_str
+  integer :: i, count_open, count_close
+  logical :: result
+
+  read *, input_str
+
+  count_open = 0
+  count_close = 0
+
+  do i = 1, len_trim(input_str)
+    if (input_str(i:i) == '(') then
+      count_open = count_open + 1
+    else if (input_str(i:i) == ')') then
+      count_close = count_close + 1
     end if
-    
-    ! Output result
-    print *, result
-    
-end program check_brackets
+  end do
+
+  result = (count_open == count_close)
+
+  print *, result
+
+end program correct_bracketing
```
