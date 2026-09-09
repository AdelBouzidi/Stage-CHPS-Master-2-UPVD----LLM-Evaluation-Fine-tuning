# Failure case: ft_ABC_source_fortran_lang_humaneval_mistral_conc20 / task 104

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_compile_err`


## Prompt

```text
Write a Fortran90 program that, given an array of positive integers, returns a sorted array (in increasing order) of all elements that do not contain any even digit.
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
    "base": 73,
    "ft": 59
  },
  "num_nonempty_lines": {
    "base": 61,
    "ft": 50
  }
}
```


## Base generated code

```fortran
program filter_odd_digits
    implicit none
    integer, parameter :: max_len = 1000
    integer :: n, i, j, temp
    integer, allocatable :: x(:), result(:)
    integer :: len_result
    integer :: digit
    
    ! Read array length
    read(*, *) n
    
    ! Read array elements
    allocate(x(n))
    read(*, *) x
    
    ! Filter elements without even digits
    len_result = 0
    do i = 1, n
        if (has_only_odd_digits(x(i))) then
            len_result = len_result + 1
        end if
    end do
    
    ! Allocate result array
    allocate(result(len_result))
    
    ! Copy filtered elements
    i = 0
    do j = 1, n
        if (has_only_odd_digits(x(j))) then
            i = i + 1
            result(i) = x(j)
        end if
    end do
    
    ! Sort result array using bubble sort
    do i = 1, len_result - 1
        do j = i + 1, len_result
            if (result(i) > result(j)) then
                temp = result(i)
                result(i) = result(j)
                result(j) = temp
            end if
        end do
    end do
    
    ! Output result
    do i = 1, len_result
        write(*, '(I0)') result(i)
    end do
    
contains
    
    ! Function to check if number has only odd digits
    function has_only_odd_digits(num) result(has_odd)
        integer, intent(in) :: num
        logical :: has_odd
        integer :: temp, digit
        
        has_odd = .true.
        temp = num
        
        do while (temp > 0)
            digit = mod(temp, 10)
            if (mod(digit, 2) == 0) then
                has_odd = .false.
                exit
            end if
            temp = temp / 10
        end do
    end function has_only_odd_digits
    
end program filter_odd_digits
```


## FT generated code

```fortran
program filter_odd_digits
    implicit none
    integer, parameter :: max_len = 100
    integer :: n, i, j, temp
    integer, allocatable :: x(:), result(:)
    integer :: len_result
    
    ! Read array length
    read(*, *) n
    
    ! Read array elements
    allocate(x(n))
    read(*, *) x
    
    ! Filter elements without even digits
    result = 0
    len_result = 0
    do i = 1, n
        if (has_only_odd_digits(x(i))) then
            len_result = len_result + 1
            result(len_result) = x(i)
        end if
    end do
    
    ! Sort the result
    do i = 1, len_result - 1
        do j = i + 1, len_result
            if (result(j) < result(i)) then
                temp = result(i)
                result(i) = result(j)
                result(j) = temp
            end if
        end do
    end do
    
    ! Output the result
    do i = 1, len_result
        write(*, '(I0)') result(i)
    end do
    
contains
    
    function has_only_odd_digits(num) result(has_odd)
        integer, intent(in) :: num
        logical :: has_odd
        integer :: digit
        
        has_odd = .true.
        do while (num > 0)
            digit = mod(num, 10)
            if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
                has_odd = .false.
                return
            end if
            num = num / 10
        end do
    end function has_only_odd_digits
    
end program filter_odd_digits
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,10 +1,9 @@
 program filter_odd_digits
     implicit none
-    integer, parameter :: max_len = 1000
+    integer, parameter :: max_len = 100
     integer :: n, i, j, temp
     integer, allocatable :: x(:), result(:)
     integer :: len_result
-    integer :: digit
     
     ! Read array length
     read(*, *) n
@@ -14,29 +13,19 @@
     read(*, *) x
     
     ! Filter elements without even digits
+    result = 0
     len_result = 0
     do i = 1, n
         if (has_only_odd_digits(x(i))) then
             len_result = len_result + 1
+            result(len_result) = x(i)
         end if
     end do
     
-    ! Allocate result array
-    allocate(result(len_result))
-    
-    ! Copy filtered elements
-    i = 0
-    do j = 1, n
-        if (has_only_odd_digits(x(j))) then
-            i = i + 1
-            result(i) = x(j)
-        end if
-    end do
-    
-    ! Sort result array using bubble sort
+    ! Sort the result
     do i = 1, len_result - 1
         do j = i + 1, len_result
-            if (result(i) > result(j)) then
+            if (result(j) < result(i)) then
                 temp = result(i)
                 result(i) = result(j)
                 result(j) = temp
@@ -44,29 +33,26 @@
         end do
     end do
     
-    ! Output result
+    ! Output the result
     do i = 1, len_result
         write(*, '(I0)') result(i)
     end do
     
 contains
     
-    ! Function to check if number has only odd digits
     function has_only_odd_digits(num) result(has_odd)
         integer, intent(in) :: num
         logical :: has_odd
-        integer :: temp, digit
+        integer :: digit
         
         has_odd = .true.
-        temp = num
-        
-        do while (temp > 0)
-            digit = mod(temp, 10)
-            if (mod(digit, 2) == 0) then
+        do while (num > 0)
+            digit = mod(num, 10)
+            if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
                 has_odd = .false.
-                exit
+                return
             end if
-            temp = temp / 10
+            num = num / 10
         end do
     end function has_only_odd_digits
     
```
