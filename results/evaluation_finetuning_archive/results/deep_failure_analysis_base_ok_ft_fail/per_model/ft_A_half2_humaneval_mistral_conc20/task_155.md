# Failure case: ft_A_half2_humaneval_mistral_conc20 / task 155

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ineq`


## Prompt

```text
Write a Fortran90 program that, given an integer, returns a tuple (pair) containing the count of even digits and the count of odd digits in the integer.
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
  "num_nonempty_lines": {
    "base": 33,
    "ft": 31
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
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
program even_odd_count
    implicit none
    integer :: num
    integer :: even_count, odd_count
    integer :: digit
    integer :: temp
    
    ! Read input
    read *, num
    
    ! Handle negative numbers by taking absolute value
    if (num < 0) then
        temp = -num
    else
        temp = num
    end if
    
    ! Count even and odd digits
    even_count = 0
    odd_count = 0
    
    if (temp == 0) then
        even_count = 1  ! 0 is even
    else
        do while (temp > 0)
            digit = mod(temp, 10)
            if (mod(digit, 2) == 0) then
                even_count = even_count + 1
            else
                odd_count = odd_count + 1
            end if
            temp = temp / 10
        end do
    end if
    
    ! Output results
    write (*, *) even_count, odd_count
    
end program even_odd_count
```


## FT generated code

```fortran
program even_odd_count_demo
    implicit none
    integer :: num
    integer :: even_count, odd_count
    
    ! Read input
    read(*,*) num
    
    ! Call the function
    call even_odd_count(num, even_count, odd_count)
    
    ! Print output
    print *, even_count, odd_count
    
contains

    subroutine even_odd_count(num, even_count, odd_count)
        implicit none
        integer, intent(in) :: num
        integer, intent(out) :: even_count, odd_count
        integer :: digit
        integer :: abs_num
        
        abs_num = abs(num)
        even_count = 0
        odd_count = 0
        
        do while (abs_num > 0)
            digit = mod(abs_num, 10)
            if (mod(digit, 2) == 0) then
                even_count = even_count + 1
            else
                odd_count = odd_count + 1
            end if
            abs_num = abs_num / 10
        end do
    end subroutine even_odd_count

end program even_odd_count_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,39 +1,39 @@
-program even_odd_count
+program even_odd_count_demo
     implicit none
     integer :: num
     integer :: even_count, odd_count
-    integer :: digit
-    integer :: temp
     
     ! Read input
-    read *, num
+    read(*,*) num
     
-    ! Handle negative numbers by taking absolute value
-    if (num < 0) then
-        temp = -num
-    else
-        temp = num
-    end if
+    ! Call the function
+    call even_odd_count(num, even_count, odd_count)
     
-    ! Count even and odd digits
-    even_count = 0
-    odd_count = 0
+    ! Print output
+    print *, even_count, odd_count
     
-    if (temp == 0) then
-        even_count = 1  ! 0 is even
-    else
-        do while (temp > 0)
-            digit = mod(temp, 10)
+contains
+
+    subroutine even_odd_count(num, even_count, odd_count)
+        implicit none
+        integer, intent(in) :: num
+        integer, intent(out) :: even_count, odd_count
+        integer :: digit
+        integer :: abs_num
+        
+        abs_num = abs(num)
+        even_count = 0
+        odd_count = 0
+        
+        do while (abs_num > 0)
+            digit = mod(abs_num, 10)
             if (mod(digit, 2) == 0) then
                 even_count = even_count + 1
             else
                 odd_count = odd_count + 1
             end if
-            temp = temp / 10
+            abs_num = abs_num / 10
         end do
-    end if
-    
-    ! Output results
-    write (*, *) even_count, odd_count
-    
-end program even_odd_count
+    end subroutine even_odd_count
+
+end program even_odd_count_demo
```
