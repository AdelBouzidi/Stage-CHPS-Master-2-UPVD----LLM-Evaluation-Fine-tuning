# Failure case: ft_AB_shuffle_humaneval_mistral_conc20 / task 104

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_modifies_intent_in_possible, static_stdin_read, status_ineq`


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
    "ft": 71
  },
  "num_nonempty_lines": {
    "base": 61,
    "ft": 60
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
  },
  "uses_print_star": {
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
program main
  implicit none
  integer :: x_len
  integer, allocatable :: x(:)
  integer, allocatable :: result(:)
  integer :: i, n

  ! Read input
  read(*,*) x_len
  allocate(x(x_len))
  read(*,*) x

  ! Call the function
  result = unique_digits(x_len, x)

  ! Output result
  print *, result

contains

  function unique_digits(x_len, x) result(res)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(x_len)
    integer, allocatable :: res(:)
    integer :: i, j, n, temp
    logical :: has_even

    ! Initialize result array
    allocate(res(x_len))
    n = 0

    ! Check each element
    do i = 1, x_len
      has_even = .false.
      temp = x(i)
      do while (temp > 0)
        if (mod(temp, 10) == 0 .or. mod(temp, 10) == 2 .or. mod(temp, 10) == 4 .or. mod(temp, 10) == 6 .or. mod(temp, 10) == 8) then
          has_even = .true.
          exit
        end if
        temp = temp / 10
      end do
      if (.not. has_even) then
        n = n + 1
        res(n) = x(i)
      end if
    end do

    ! Sort the result
    call sort_array(res, n)

  end function unique_digits

  subroutine sort_array(arr, n)
    implicit none
    integer, intent(inout) :: arr(:)
    integer, intent(in) :: n
    integer :: i, j, temp
    do i = 1, n-1
      do j = 1, n-i
        if (arr(j) > arr(j+1)) then
          temp = arr(j)
          arr(j) = arr(j+1)
          arr(j+1) = temp
        end if
      end do
    end do
  end subroutine sort_array

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,73 +1,71 @@
-program filter_odd_digits
+program main
+  implicit none
+  integer :: x_len
+  integer, allocatable :: x(:)
+  integer, allocatable :: result(:)
+  integer :: i, n
+
+  ! Read input
+  read(*,*) x_len
+  allocate(x(x_len))
+  read(*,*) x
+
+  ! Call the function
+  result = unique_digits(x_len, x)
+
+  ! Output result
+  print *, result
+
+contains
+
+  function unique_digits(x_len, x) result(res)
     implicit none
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
+    integer, intent(in) :: x_len
+    integer, intent(in) :: x(x_len)
+    integer, allocatable :: res(:)
+    integer :: i, j, n, temp
+    logical :: has_even
+
+    ! Initialize result array
+    allocate(res(x_len))
+    n = 0
+
+    ! Check each element
+    do i = 1, x_len
+      has_even = .false.
+      temp = x(i)
+      do while (temp > 0)
+        if (mod(temp, 10) == 0 .or. mod(temp, 10) == 2 .or. mod(temp, 10) == 4 .or. mod(temp, 10) == 6 .or. mod(temp, 10) == 8) then
+          has_even = .true.
+          exit
         end if
+        temp = temp / 10
+      end do
+      if (.not. has_even) then
+        n = n + 1
+        res(n) = x(i)
+      end if
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
+
+    ! Sort the result
+    call sort_array(res, n)
+
+  end function unique_digits
+
+  subroutine sort_array(arr, n)
+    implicit none
+    integer, intent(inout) :: arr(:)
+    integer, intent(in) :: n
+    integer :: i, j, temp
+    do i = 1, n-1
+      do j = 1, n-i
+        if (arr(j) > arr(j+1)) then
+          temp = arr(j)
+          arr(j) = arr(j+1)
+          arr(j+1) = temp
         end if
+      end do
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
+  end subroutine sort_array
+
+end program main
```
