# Failure case: ft_AC_shuffle_humaneval_mistral_conc3 / task 104

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
    "ft": 62
  },
  "num_nonempty_lines": {
    "base": 61,
    "ft": 53
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
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
  integer, allocatable :: x(:)
  integer :: x_len
  integer, allocatable :: result(:)
  integer :: i, j, n, idx
  integer :: temp

  ! Read input
  read(*,*) x_len
  read(*,*) x

  ! Initialize result array
  allocate(result(x_len))
  n = 0

  ! Filter numbers that don't contain even digits
  do i = 1, x_len
    if (has_no_even_digit(x(i))) then
      n = n + 1
      result(n) = x(i)
    end if
  end do

  ! Sort the result array
  call sort_array(result, n)

  ! Output the result
  write(*,*) result(1:n)

contains

  logical function has_no_even_digit(num)
    integer, intent(in) :: num
    integer :: digit
    has_no_even_digit = .true.
    do while (num > 0)
      digit = mod(num, 10)
      if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
        has_no_even_digit = .false.
        return
      end if
      num = num / 10
    end do
  end function has_no_even_digit

  subroutine sort_array(arr, n)
    integer, intent(inout) :: arr(:)
    integer, intent(in) :: n
    integer :: i, j, temp
    do i = 1, n-1
      do j = i+1, n
        if (arr(j) < arr(i)) then
          temp = arr(i)
          arr(i) = arr(j)
          arr(j) = temp
        end if
      end do
    end do
  end subroutine sort_array

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
+  integer, allocatable :: x(:)
+  integer :: x_len
+  integer, allocatable :: result(:)
+  integer :: i, j, n, idx
+  integer :: temp
+
+  ! Read input
+  read(*,*) x_len
+  read(*,*) x
+
+  ! Initialize result array
+  allocate(result(x_len))
+  n = 0
+
+  ! Filter numbers that don't contain even digits
+  do i = 1, x_len
+    if (has_no_even_digit(x(i))) then
+      n = n + 1
+      result(n) = x(i)
+    end if
+  end do
+
+  ! Sort the result array
+  call sort_array(result, n)
+
+  ! Output the result
+  write(*,*) result(1:n)
+
+contains
+
+  logical function has_no_even_digit(num)
+    integer, intent(in) :: num
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
+    has_no_even_digit = .true.
+    do while (num > 0)
+      digit = mod(num, 10)
+      if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
+        has_no_even_digit = .false.
+        return
+      end if
+      num = num / 10
+    end do
+  end function has_no_even_digit
+
+  subroutine sort_array(arr, n)
+    integer, intent(inout) :: arr(:)
+    integer, intent(in) :: n
+    integer :: i, j, temp
+    do i = 1, n-1
+      do j = i+1, n
+        if (arr(j) < arr(i)) then
+          temp = arr(i)
+          arr(i) = arr(j)
+          arr(j) = temp
         end if
+      end do
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
+  end subroutine sort_array
+
+end program unique_digits
```
