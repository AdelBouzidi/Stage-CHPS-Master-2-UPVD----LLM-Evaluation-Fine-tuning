# Failure case: ft_ABC_filtered_manual_humaneval_mistral_conc20 / task 159

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


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
  "has_program": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 22,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 19,
    "ft": 0
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  },
  "uses_implicit_none": {
    "base": true,
    "ft": false
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

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,22 +0,0 @@
-program hungry_rabbit
-    implicit none
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
-    else
-        total_eaten = already_eaten + remaining
-        carrots_left = 0
-    end if
-    
-    ! Output the result
-    write (*, *) total_eaten, carrots_left
-end program hungry_rabbit
```
