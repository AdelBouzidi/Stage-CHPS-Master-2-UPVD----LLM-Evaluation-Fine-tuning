# Failure case: ft_AB_shuffle_humaneval_mistral_conc3 / task 107

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


## Prompt

```text
Write a Fortran90 program that, given a positive integer n, counts the number of even and odd integer palindromes within the range [1, n] inclusive, and returns the result as a pair (even_count, odd_count).
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
    "base": 35,
    "ft": 46
  },
  "num_nonempty_lines": {
    "base": 31,
    "ft": 39
  },
  "uses_read_stdin": {
    "base": false,
    "ft": true
  }
}
```


## Base generated code

```fortran
program even_odd_palindrome
    implicit none
    integer :: n
    integer :: i
    integer :: even_count = 0
    integer :: odd_count = 0
    integer :: temp
    integer :: reversed_num
    integer :: digit
    
    ! Read input
    read *, n
    
    ! Check each number from 1 to n
    do i = 1, n
        temp = i
        reversed_num = 0
        do while (temp > 0)
            digit = mod(temp, 10)
            reversed_num = reversed_num * 10 + digit
            temp = temp / 10
        end do
        
        if (i == reversed_num) then
            if (mod(i, 2) == 0) then
                even_count = even_count + 1
            else
                odd_count = odd_count + 1
            end if
        end if
    end do
    
    ! Output results
    print *, even_count, odd_count
end program even_odd_palindrome
```


## FT generated code

```fortran
program even_odd_palindrome
    implicit none
    integer :: n
    integer :: even_count, odd_count
    integer :: i
    logical :: is_palindrome

    ! Read input
    read(*,*) n

    ! Initialize counters
    even_count = 0
    odd_count = 0

    ! Check each number from 1 to n
    do i = 1, n
        if (is_palindrome(i)) then
            if (mod(i, 2) == 0) then
                even_count = even_count + 1
            else
                odd_count = odd_count + 1
            end if
        end if
    end do

    ! Output results
    print *, even_count, odd_count

contains

    logical function is_palindrome(num)
        integer, intent(in) :: num
        integer :: temp
        integer :: reversed
        integer :: digit
        reversed = 0
        temp = num
        do while (temp > 0)
            digit = mod(temp, 10)
            reversed = reversed * 10 + digit
            temp = temp / 10
        end do
        is_palindrome = (reversed == num)
    end function is_palindrome

end program even_odd_palindrome
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,27 +1,20 @@
 program even_odd_palindrome
     implicit none
     integer :: n
+    integer :: even_count, odd_count
     integer :: i
-    integer :: even_count = 0
-    integer :: odd_count = 0
-    integer :: temp
-    integer :: reversed_num
-    integer :: digit
-    
+    logical :: is_palindrome
+
     ! Read input
-    read *, n
-    
+    read(*,*) n
+
+    ! Initialize counters
+    even_count = 0
+    odd_count = 0
+
     ! Check each number from 1 to n
     do i = 1, n
-        temp = i
-        reversed_num = 0
-        do while (temp > 0)
-            digit = mod(temp, 10)
-            reversed_num = reversed_num * 10 + digit
-            temp = temp / 10
-        end do
-        
-        if (i == reversed_num) then
+        if (is_palindrome(i)) then
             if (mod(i, 2) == 0) then
                 even_count = even_count + 1
             else
@@ -29,7 +22,25 @@
             end if
         end if
     end do
-    
+
     ! Output results
     print *, even_count, odd_count
+
+contains
+
+    logical function is_palindrome(num)
+        integer, intent(in) :: num
+        integer :: temp
+        integer :: reversed
+        integer :: digit
+        reversed = 0
+        temp = num
+        do while (temp > 0)
+            digit = mod(temp, 10)
+            reversed = reversed * 10 + digit
+            temp = temp / 10
+        end do
+        is_palindrome = (reversed == num)
+    end function is_palindrome
+
 end program even_odd_palindrome
```
