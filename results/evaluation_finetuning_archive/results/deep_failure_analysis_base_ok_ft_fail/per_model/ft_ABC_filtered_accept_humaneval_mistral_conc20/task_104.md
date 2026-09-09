# Failure case: ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 104

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
  "has_debug_words": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 73,
    "ft": 62
  },
  "num_nonempty_lines": {
    "base": 61,
    "ft": 54
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
program unique_digits
  implicit none
  integer :: x_len
  integer, allocatable :: x(:)
  integer :: result_len
  integer, allocatable :: result(:)
  integer :: i, j, k
  integer :: temp

  ! Read input
  read(*,*) x_len
  allocate(x(x_len))
  read(*,*) x

  ! Process the array
  result_len = 0
  do i = 1, x_len
    if (contains_only_odd_digits(x(i))) then
      result_len = result_len + 1
    end if
  end do

  allocate(result(result_len))
  k = 0
  do i = 1, x_len
    if (contains_only_odd_digits(x(i))) then
      k = k + 1
      result(k) = x(i)
    end if
  end do

  ! Sort the result
  do i = 1, result_len - 1
    do j = i + 1, result_len
      if (result(i) > result(j)) then
        temp = result(i)
        result(i) = result(j)
        result(j) = temp
      end if
    end do
  end do

  ! Output the result
  write(*,*) result

contains

  logical function contains_only_odd_digits(n)
    integer, intent(in) :: n
    integer :: digit
    contains_only_odd_digits = .true.
    do while (n > 0)
      digit = mod(n, 10)
      if (mod(digit, 2) == 0) then
        contains_only_odd_digits = .false.
        return
      end if
      n = n / 10
    end do
  end function contains_only_odd_digits

end program unique_digits
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,73 +1,62 @@
-program filter_odd_digits
-    implicit none
-    integer, parameter :: max_len = 1000
-    integer :: n, i, j, temp
-    integer, allocatable :: x(:), result(:)
-    integer :: len_result
+program unique_digits
+  implicit none
+  integer :: x_len
+  integer, allocatable :: x(:)
+  integer :: result_len
+  integer, allocatable :: result(:)
+  integer :: i, j, k
+  integer :: temp
+
+  ! Read input
+  read(*,*) x_len
+  allocate(x(x_len))
+  read(*,*) x
+
+  ! Process the array
+  result_len = 0
+  do i = 1, x_len
+    if (contains_only_odd_digits(x(i))) then
+      result_len = result_len + 1
+    end if
+  end do
+
+  allocate(result(result_len))
+  k = 0
+  do i = 1, x_len
+    if (contains_only_odd_digits(x(i))) then
+      k = k + 1
+      result(k) = x(i)
+    end if
+  end do
+
+  ! Sort the result
+  do i = 1, result_len - 1
+    do j = i + 1, result_len
+      if (result(i) > result(j)) then
+        temp = result(i)
+        result(i) = result(j)
+        result(j) = temp
+      end if
+    end do
+  end do
+
+  ! Output the result
+  write(*,*) result
+
+contains
+
+  logical function contains_only_odd_digits(n)
+    integer, intent(in) :: n
     integer :: digit
-    
-    ! Read array length
-    read(*, *) n
-    
-    ! Read array elements
-    allocate(x(n))
-    read(*, *) x
-    
-    ! Filter elements without even digits
-    len_result = 0
-    do i = 1, n
-        if (has_only_odd_digits(x(i))) then
-            len_result = len_result + 1
-        end if
+    contains_only_odd_digits = .true.
+    do while (n > 0)
+      digit = mod(n, 10)
+      if (mod(digit, 2) == 0) then
+        contains_only_odd_digits = .false.
+        return
+      end if
+      n = n / 10
     end do
-    
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
-    do i = 1, len_result - 1
-        do j = i + 1, len_result
-            if (result(i) > result(j)) then
-                temp = result(i)
-                result(i) = result(j)
-                result(j) = temp
-            end if
-        end do
-    end do
-    
-    ! Output result
-    do i = 1, len_result
-        write(*, '(I0)') result(i)
-    end do
-    
-contains
-    
-    ! Function to check if number has only odd digits
-    function has_only_odd_digits(num) result(has_odd)
-        integer, intent(in) :: num
-        logical :: has_odd
-        integer :: temp, digit
-        
-        has_odd = .true.
-        temp = num
-        
-        do while (temp > 0)
-            digit = mod(temp, 10)
-            if (mod(digit, 2) == 0) then
-                has_odd = .false.
-                exit
-            end if
-            temp = temp / 10
-        end do
-    end function has_only_odd_digits
-    
-end program filter_odd_digits
+  end function contains_only_odd_digits
+
+end program unique_digits
```
