# Failure case: ft_A_humaneval_mistral_conc3 / task 104

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `static_modifies_intent_in_possible, status_compile_err`


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
    "ft": 64
  },
  "num_nonempty_lines": {
    "base": 61,
    "ft": 57
  },
  "uses_hardcoded_arrays": {
    "base": false,
    "ft": true
  },
  "uses_print_star": {
    "base": false,
    "ft": true
  },
  "uses_read_stdin": {
    "base": true,
    "ft": false
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
  integer :: i, j, k, n, len
  integer :: temp
  character(len=1) :: c
  logical :: has_even

  ! Hardcoded input as per example
  x_len = 4
  allocate(x(x_len))
  x = [15, 33, 1422, 1]

  ! Call the function
  result = unique_digits(x_len, x)

  ! Output the result
  print *, result

contains

  function unique_digits(x_len, x) result(res)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(x_len)
    integer, allocatable :: res(:)
    integer :: i, j, k, n, len
    integer :: temp
    character(len=1) :: c
    logical :: has_even

    ! Initialize result array
    allocate(res(x_len))
    n = 0
    do i = 1, x_len
      has_even = .false.
      len = len(str(x(i)))
      do j = 1, len
        c = achar(iachar(achar(j:j)))
        if (mod(iachar(c), 2) == 0) then
          has_even = .true.
          exit
        end if
      end do
      if (.not. has_even) then
        n = n + 1
        res(n) = x(i)
      end if
    end do
    ! Sort the result
    do i = 1, n-1
      do j = i+1, n
        if (res(i) > res(j)) then
          temp = res(i)
          res(i) = res(j)
          res(j) = temp
        end if
      end do
    end do
  end function unique_digits

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,73 +1,64 @@
-program filter_odd_digits
+program main
+  implicit none
+  integer :: x_len
+  integer, allocatable :: x(:)
+  integer, allocatable :: result(:)
+  integer :: i, j, k, n, len
+  integer :: temp
+  character(len=1) :: c
+  logical :: has_even
+
+  ! Hardcoded input as per example
+  x_len = 4
+  allocate(x(x_len))
+  x = [15, 33, 1422, 1]
+
+  ! Call the function
+  result = unique_digits(x_len, x)
+
+  ! Output the result
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
+    integer :: i, j, k, n, len
+    integer :: temp
+    character(len=1) :: c
+    logical :: has_even
+
+    ! Initialize result array
+    allocate(res(x_len))
+    n = 0
+    do i = 1, x_len
+      has_even = .false.
+      len = len(str(x(i)))
+      do j = 1, len
+        c = achar(iachar(achar(j:j)))
+        if (mod(iachar(c), 2) == 0) then
+          has_even = .true.
+          exit
         end if
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
+    ! Sort the result
+    do i = 1, n-1
+      do j = i+1, n
+        if (res(i) > res(j)) then
+          temp = res(i)
+          res(i) = res(j)
+          res(j) = temp
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
+  end function unique_digits
+
+end program main
```
