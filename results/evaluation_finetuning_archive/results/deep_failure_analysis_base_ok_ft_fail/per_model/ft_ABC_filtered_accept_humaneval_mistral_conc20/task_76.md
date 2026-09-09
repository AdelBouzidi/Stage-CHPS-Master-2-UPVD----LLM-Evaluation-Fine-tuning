# Failure case: ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 76

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ineq`


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
  "has_debug_words": {
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
    "ft": 54
  },
  "num_nonempty_lines": {
    "base": 58,
    "ft": 43
  },
  "uses_read_stdin": {
    "base": false,
    "ft": true
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
program is_simple_power_demo
  implicit none
  integer :: x, n
  logical :: result

  ! Read input
  read(*,*) x
  read(*,*) n

  ! Call the function
  result = is_simple_power(x, n)

  ! Output result
  print *, result

contains

  function is_simple_power(x, n) result(res)
    implicit none
    integer, intent(in) :: x, n
    logical :: res
    integer :: i

    if (n == 0) then
      res = .false.
      return
    end if

    if (x == 0) then
      res = .false.
      return
    end if

    if (x < 0) then
      if (mod(x, n) /= 0) then
        res = .false.
        return
      end if
    end if

    res = .true.
    do i = 1, 30
      if (x == n**i) then
        exit
      end if
      if (x < n**i) then
        res = .false.
        exit
      end if
    end do

  end function is_simple_power

end program is_simple_power_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,61 +1,54 @@
-program is_simple_power
+program is_simple_power_demo
+  implicit none
+  integer :: x, n
+  logical :: result
+
+  ! Read input
+  read(*,*) x
+  read(*,*) n
+
+  ! Call the function
+  result = is_simple_power(x, n)
+
+  ! Output result
+  print *, result
+
+contains
+
+  function is_simple_power(x, n) result(res)
     implicit none
-    integer :: x, n
-    integer :: k
-    integer :: temp
-    
-    ! Read input
-    read *, x
-    read *, n
-    
-    ! Check if x is a simple power of n
+    integer, intent(in) :: x, n
+    logical :: res
+    integer :: i
+
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
+      res = .false.
+      return
     end if
-    
-end program is_simple_power
+
+    if (x == 0) then
+      res = .false.
+      return
+    end if
+
+    if (x < 0) then
+      if (mod(x, n) /= 0) then
+        res = .false.
+        return
+      end if
+    end if
+
+    res = .true.
+    do i = 1, 30
+      if (x == n**i) then
+        exit
+      end if
+      if (x < n**i) then
+        res = .false.
+        exit
+      end if
+    end do
+
+  end function is_simple_power
+
+end program is_simple_power_demo
```
