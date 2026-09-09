# Failure case: ft_ABC_source_stack_v1_humaneval_mistral_conc20 / task 76

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


## Prompt

```text
Write a Fortran90 program that returns true if a given integer x is a simple power of n and false otherwise.
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
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 61,
    "ft": 12
  },
  "num_nonempty_lines": {
    "base": 58,
    "ft": 9
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program is_simple_power
    implicit none
    integer :: x, n
    integer :: k
    integer :: temp
    
    ! Read input
    read *, x
    read *, n
    
    ! Check if x is a simple power of n
    if (n == 0) then
        if (x == 0) then
            print *, .true.
        else
            print *, .false.
        end if
    else if (n == 1) then
        if (x == 1) then
            print *, .true.
        else
            print *, .false.
        end if
    else if (x == 1) then
        print *, .true.
    else if (x < 0) then
        if (n < 0) then
            ! Check if x is a power of n with even exponent
            temp = abs(x)
            k = 0
            do while (n**k < temp)
                k = k + 1
                if (n**k > temp) exit
            end do
            if (n**k == temp) then
                if (mod(k, 2) == 0) then
                    print *, .true.
                else
                    print *, .false.
                end if
            else
                print *, .false.
            end if
        else
            print *, .false.
        end if
    else
        ! x > 0 and n > 0
        k = 0
        do while (n**k < x)
            k = k + 1
            if (n**k > x) exit
        end do
        if (n**k == x) then
            print *, .true.
        else
            print *, .false.
        end if
    end if
    
end program is_simple_power
```


## FT generated code

```fortran
program main
  implicit none
  integer :: x, n
  logical :: result

  read *, x
  read *, n

  result = is_simple_power(x, n)

  print *, result
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,61 +1,12 @@
-program is_simple_power
-    implicit none
-    integer :: x, n
-    integer :: k
-    integer :: temp
-    
-    ! Read input
-    read *, x
-    read *, n
-    
-    ! Check if x is a simple power of n
-    if (n == 0) then
-        if (x == 0) then
-            print *, .true.
-        else
-            print *, .false.
-        end if
-    else if (n == 1) then
-        if (x == 1) then
-            print *, .true.
-        else
-            print *, .false.
-        end if
-    else if (x == 1) then
-        print *, .true.
-    else if (x < 0) then
-        if (n < 0) then
-            ! Check if x is a power of n with even exponent
-            temp = abs(x)
-            k = 0
-            do while (n**k < temp)
-                k = k + 1
-                if (n**k > temp) exit
-            end do
-            if (n**k == temp) then
-                if (mod(k, 2) == 0) then
-                    print *, .true.
-                else
-                    print *, .false.
-                end if
-            else
-                print *, .false.
-            end if
-        else
-            print *, .false.
-        end if
-    else
-        ! x > 0 and n > 0
-        k = 0
-        do while (n**k < x)
-            k = k + 1
-            if (n**k > x) exit
-        end do
-        if (n**k == x) then
-            print *, .true.
-        else
-            print *, .false.
-        end if
-    end if
-    
-end program is_simple_power
+program main
+  implicit none
+  integer :: x, n
+  logical :: result
+
+  read *, x
+  read *, n
+
+  result = is_simple_power(x, n)
+
+  print *, result
+end program main
```
