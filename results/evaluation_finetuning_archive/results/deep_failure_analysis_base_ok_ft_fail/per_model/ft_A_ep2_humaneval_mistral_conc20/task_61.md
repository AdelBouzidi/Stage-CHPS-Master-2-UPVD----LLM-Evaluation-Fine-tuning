# Failure case: ft_A_ep2_humaneval_mistral_conc20 / task 61

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
    "ft": 31
  },
  "num_nonempty_lines": {
    "base": 29,
    "ft": 25
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
  logical :: result
  integer :: i, count

  ! Read input from stdin
  read *, input_str

  ! Initialize count for tracking brackets
  count = 0

  ! Check each character in the string
  do i = 1, len_trim(input_str)
    select case (input_str(i:i))
    case ('(')
      count = count + 1
    case (')')
      count = count - 1
    case default
      ! Ignore other characters
    end select
  end do

  ! Check if all brackets are matched
  result = (count == 0)

  ! Output the result
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
-    end if
-    
-    ! Output result
-    print *, result
-    
-end program check_brackets
+program correct_bracketing
+  implicit none
+  character(len=100) :: input_str
+  logical :: result
+  integer :: i, count
+
+  ! Read input from stdin
+  read *, input_str
+
+  ! Initialize count for tracking brackets
+  count = 0
+
+  ! Check each character in the string
+  do i = 1, len_trim(input_str)
+    select case (input_str(i:i))
+    case ('(')
+      count = count + 1
+    case (')')
+      count = count - 1
+    case default
+      ! Ignore other characters
+    end select
+  end do
+
+  ! Check if all brackets are matched
+  result = (count == 0)
+
+  ! Output the result
+  print *, result
+
+end program correct_bracketing
```
