# Failure case: ft_AC_antineighbor_humaneval_mistral_conc20 / task 104

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
    "ft": 81
  },
  "num_nonempty_lines": {
    "base": 61,
    "ft": 71
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
  integer :: n, i, j, k, len

  ! Read input
  read(*,*) x_len
  allocate(x(x_len))
  read(*,*) x

  ! Call the function
  call unique_digits(x_len, x, result, n)

  ! Output result
  print *, n
  print *, result

contains

  subroutine unique_digits(x_len, x, result, n)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(x_len)
    integer, intent(out) :: result(:)
    integer, intent(out) :: n
    integer :: i, j, k, len
    logical :: has_even

    n = 0
    do i = 1, x_len
      has_even = .false.
      do j = 1, len(x(i))
        if (mod(x(i), 10) == 0) then
          has_even = .true.
          exit
        end if
      end do
      if (.not. has_even) then
        n = n + 1
      end if
    end do

    allocate(result(n))
    k = 0
    do i = 1, x_len
      has_even = .false.
      do j = 1, len(x(i))
        if (mod(x(i), 10) == 0) then
          has_even = .true.
          exit
        end if
      end do
      if (.not. has_even) then
        k = k + 1
        result(k) = x(i)
      end if
    end do

    result = sort(result)
  end subroutine unique_digits

  function sort(arr) result(sorted)
    implicit none
    integer, intent(in) :: arr(:)
    integer :: sorted(:)
    integer :: i, j, temp
    sorted = arr
    do i = 1, size(sorted) - 1
      do j = i + 1, size(sorted)
        if (sorted(j) < sorted(i)) then
          temp = sorted(i)
          sorted(i) = sorted(j)
          sorted(j) = temp
        end if
      end do
    end do
  end function sort

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,73 +1,81 @@
-program filter_odd_digits
+program main
+  implicit none
+  integer :: x_len
+  integer, allocatable :: x(:)
+  integer, allocatable :: result(:)
+  integer :: n, i, j, k, len
+
+  ! Read input
+  read(*,*) x_len
+  allocate(x(x_len))
+  read(*,*) x
+
+  ! Call the function
+  call unique_digits(x_len, x, result, n)
+
+  ! Output result
+  print *, n
+  print *, result
+
+contains
+
+  subroutine unique_digits(x_len, x, result, n)
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
+    integer, intent(out) :: result(:)
+    integer, intent(out) :: n
+    integer :: i, j, k, len
+    logical :: has_even
+
+    n = 0
+    do i = 1, x_len
+      has_even = .false.
+      do j = 1, len(x(i))
+        if (mod(x(i), 10) == 0) then
+          has_even = .true.
+          exit
         end if
+      end do
+      if (.not. has_even) then
+        n = n + 1
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
+    allocate(result(n))
+    k = 0
+    do i = 1, x_len
+      has_even = .false.
+      do j = 1, len(x(i))
+        if (mod(x(i), 10) == 0) then
+          has_even = .true.
+          exit
         end if
+      end do
+      if (.not. has_even) then
+        k = k + 1
+        result(k) = x(i)
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
+
+    result = sort(result)
+  end subroutine unique_digits
+
+  function sort(arr) result(sorted)
+    implicit none
+    integer, intent(in) :: arr(:)
+    integer :: sorted(:)
+    integer :: i, j, temp
+    sorted = arr
+    do i = 1, size(sorted) - 1
+      do j = i + 1, size(sorted)
+        if (sorted(j) < sorted(i)) then
+          temp = sorted(i)
+          sorted(i) = sorted(j)
+          sorted(j) = temp
+        end if
+      end do
     end do
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
+  end function sort
+
+end program main
```
