# Failure case: ft_A_half1_humaneval_mistral_conc20 / task 159

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_compile_err`


## Prompt

```text
Write a Fortran90 program that simulates a hungry rabbit. Given the number of carrots already eaten, the number of carrots needed, and the number of remaining carrots available, return an array of two integers: the total carrots eaten after the meal and the carrots left. If there are not enough remaining carrots, the rabbit eats all and remains hungry.
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
  "has_debug_words": {
    "base": false,
    "ft": true
  },
  "num_functions": {
    "base": 0,
    "ft": 2
  },
  "num_lines": {
    "base": 22,
    "ft": 32
  },
  "num_nonempty_lines": {
    "base": 19,
    "ft": 26
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  },
  "uses_print_star": {
    "base": false,
    "ft": true
  },
  "uses_read_stdin": {
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
program hungry_rabbit
    implicit none
    integer :: already_eaten, needed, remaining
    integer :: total_eaten, carrots_left
    
    ! Read input values
    read *, already_eaten
    read *, needed
    read *, remaining
    
    ! Calculate total eaten and remaining carrots
    if (remaining >= needed) then
        total_eaten = already_eaten + needed
        carrots_left = remaining - needed
    else
        total_eaten = already_eaten + remaining
        carrots_left = 0
    end if
    
    ! Output the result
    write (*, *) total_eaten, carrots_left
end program hungry_rabbit
```


## FT generated code

```fortran
program rabbit
  implicit none
  integer :: number, need, remaining
  integer, dimension(2) :: result

  ! Read input
  read(*,*) number
  read(*,*) need
  read(*,*) remaining

  ! Call the eat function
  result = eat(number, need, remaining)

  ! Output result
  print *, result(1), result(2)

contains

  function eat(number, need, remaining) result(res)
    implicit none
    integer, intent(in) :: number, need, remaining
    integer, dimension(2), intent(out) :: res
    if (remaining >= need) then
      res(1) = number + need
      res(2) = remaining - need
    else
      res(1) = number + remaining
      res(2) = 0
    end if
  end function eat

end program rabbit
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,22 +1,32 @@
-program hungry_rabbit
+program rabbit
+  implicit none
+  integer :: number, need, remaining
+  integer, dimension(2) :: result
+
+  ! Read input
+  read(*,*) number
+  read(*,*) need
+  read(*,*) remaining
+
+  ! Call the eat function
+  result = eat(number, need, remaining)
+
+  ! Output result
+  print *, result(1), result(2)
+
+contains
+
+  function eat(number, need, remaining) result(res)
     implicit none
-    integer :: already_eaten, needed, remaining
-    integer :: total_eaten, carrots_left
-    
-    ! Read input values
-    read *, already_eaten
-    read *, needed
-    read *, remaining
-    
-    ! Calculate total eaten and remaining carrots
-    if (remaining >= needed) then
-        total_eaten = already_eaten + needed
-        carrots_left = remaining - needed
+    integer, intent(in) :: number, need, remaining
+    integer, dimension(2), intent(out) :: res
+    if (remaining >= need) then
+      res(1) = number + need
+      res(2) = remaining - need
     else
-        total_eaten = already_eaten + remaining
-        carrots_left = 0
+      res(1) = number + remaining
+      res(2) = 0
     end if
-    
-    ! Output the result
-    write (*, *) total_eaten, carrots_left
-end program hungry_rabbit
+  end function eat
+
+end program rabbit
```
