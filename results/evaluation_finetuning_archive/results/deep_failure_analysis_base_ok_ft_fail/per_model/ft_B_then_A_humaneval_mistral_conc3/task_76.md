# Failure case: ft_B_then_A_humaneval_mistral_conc3 / task 76

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


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
    "base": 61,
    "ft": 32
  },
  "num_nonempty_lines": {
    "base": 58,
    "ft": 32
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
  integer :: x
  read *, x
  print *, is_simple_power(x, 2)
contains
  logical function is_simple_power(x, n)
    integer, intent(in) :: x, n
    if (n == 0) then
      if (x == 1) then
        is_simple_power = .true.
      else
        is_simple_power = .false.
      end if
    else
      if (x == 1) then
        is_simple_power = .true.
      else if (x == 0) then
        is_simple_power = .false.
      else
        do while (x /= 1)
          if (mod(x, n) /= 0) then
            is_simple_power = .false.
            exit
          end if
          x = x / n
        end do
        is_simple_power = (x == 1)
      end if
    end if
  end function is_simple_power
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,61 +1,32 @@
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
+program main
+  implicit none
+  integer :: x
+  read *, x
+  print *, is_simple_power(x, 2)
+contains
+  logical function is_simple_power(x, n)
+    integer, intent(in) :: x, n
     if (n == 0) then
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
+      if (x == 1) then
+        is_simple_power = .true.
+      else
+        is_simple_power = .false.
+      end if
     else
-        ! x > 0 and n > 0
-        k = 0
-        do while (n**k < x)
-            k = k + 1
-            if (n**k > x) exit
+      if (x == 1) then
+        is_simple_power = .true.
+      else if (x == 0) then
+        is_simple_power = .false.
+      else
+        do while (x /= 1)
+          if (mod(x, n) /= 0) then
+            is_simple_power = .false.
+            exit
+          end if
+          x = x / n
         end do
-        if (n**k == x) then
-            print *, .true.
-        else
-            print *, .false.
-        end if
+        is_simple_power = (x == 1)
+      end if
     end if
-    
-end program is_simple_power
+  end function is_simple_power
+end program main
```
