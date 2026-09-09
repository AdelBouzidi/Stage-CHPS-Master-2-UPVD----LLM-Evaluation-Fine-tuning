# Failure case: ft_ABC_source_burkardt_humaneval_mistral_conc20 / task 104

- Base status: `ok`

- FT status: `runtime_err`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_stdin_read, status_runtime_err`


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
  "has_contains": {
    "base": true,
    "ft": false
  },
  "has_debug_words": {
    "base": true,
    "ft": false
  },
  "modifies_intent_in_possible": {
    "base": true,
    "ft": false
  },
  "num_functions": {
    "base": 2,
    "ft": 0
  },
  "num_lines": {
    "base": 73,
    "ft": 52
  },
  "num_nonempty_lines": {
    "base": 61,
    "ft": 46
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
  integer :: i, j, temp
  integer :: n, digit
  logical :: even_digit_found

  ! Read input
  read(*,*) x_len
  allocate(x(x_len))
  read(*,*) x

  ! Process each number
  result_len = 0
  allocate(result(result_len))

  do i = 1, x_len
    n = x(i)
    even_digit_found = .false.
    do while (n > 0)
      digit = mod(n, 10)
      if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
        even_digit_found = .true.
        exit
      end if
      n = n / 10
    end do
    if (.not. even_digit_found) then
      result_len = result_len + 1
      allocate(result(result_len))
      result(result_len) = x(i)
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

end program unique_digits
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,73 +1,52 @@
-program filter_odd_digits
-    implicit none
-    integer, parameter :: max_len = 1000
-    integer :: n, i, j, temp
-    integer, allocatable :: x(:), result(:)
-    integer :: len_result
-    integer :: digit
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
+program unique_digits
+  implicit none
+  integer :: x_len
+  integer, allocatable :: x(:)
+  integer :: result_len
+  integer, allocatable :: result(:)
+  integer :: i, j, temp
+  integer :: n, digit
+  logical :: even_digit_found
+
+  ! Read input
+  read(*,*) x_len
+  allocate(x(x_len))
+  read(*,*) x
+
+  ! Process each number
+  result_len = 0
+  allocate(result(result_len))
+
+  do i = 1, x_len
+    n = x(i)
+    even_digit_found = .false.
+    do while (n > 0)
+      digit = mod(n, 10)
+      if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
+        even_digit_found = .true.
+        exit
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
+    if (.not. even_digit_found) then
+      result_len = result_len + 1
+      allocate(result(result_len))
+      result(result_len) = x(i)
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
     end do
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
+  end do
+
+  ! Output the result
+  write(*,*) result
+
+end program unique_digits
```
