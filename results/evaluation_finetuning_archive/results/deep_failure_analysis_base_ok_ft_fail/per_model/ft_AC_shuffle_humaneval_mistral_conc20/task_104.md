# Failure case: ft_AC_shuffle_humaneval_mistral_conc20 / task 104

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_output_labels`

- Labels: `static_modifies_intent_in_possible, static_output_labels, status_ineq`


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
  "has_labels_in_output": {
    "base": false,
    "ft": true
  },
  "num_functions": {
    "base": 2,
    "ft": 0
  },
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
    "ft": 2
  },
  "uses_assumed_size": {
    "base": false,
    "ft": true
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
program unique_digits_demo
  implicit none
  integer :: x_len
  integer, allocatable :: x(:)
  integer, allocatable :: result(:)
  integer :: i, n

  ! Hardcoded input for demonstration
  x_len = 4
  allocate(x(x_len))
  x = [15, 33, 1422, 1]

  call unique_digits(x_len, x, result)

  print *, 'Result:', result

contains

  subroutine unique_digits(x_len, x, result)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(*)
    integer, allocatable, intent(out) :: result(:)
    integer :: i, n, temp
    integer :: digits(10)
    integer :: num, digit

    n = 0
    do i = 1, x_len
      num = x(i)
      digits = 0
      do while (num > 0)
        digit = mod(num, 10)
        if (mod(digit, 2) == 0) then
          digits(digit) = 1
        end if
        num = num / 10
      end do
      if (sum(digits) == 0) then
        n = n + 1
      end if
    end do

    allocate(result(n))
    n = 0
    do i = 1, x_len
      num = x(i)
      digits = 0
      do while (num > 0)
        digit = mod(num, 10)
        if (mod(digit, 2) == 0) then
          digits(digit) = 1
        end if
        num = num / 10
      end do
      if (sum(digits) == 0) then
        n = n + 1
        result(n) = x(i)
      end if
    end do

    call sort(result, n)
  end subroutine unique_digits

  subroutine sort(arr, n)
    implicit none
    integer, intent(inout) :: arr(*)
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
  end subroutine sort

end program unique_digits_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,73 +1,81 @@
-program filter_odd_digits
+program unique_digits_demo
+  implicit none
+  integer :: x_len
+  integer, allocatable :: x(:)
+  integer, allocatable :: result(:)
+  integer :: i, n
+
+  ! Hardcoded input for demonstration
+  x_len = 4
+  allocate(x(x_len))
+  x = [15, 33, 1422, 1]
+
+  call unique_digits(x_len, x, result)
+
+  print *, 'Result:', result
+
+contains
+
+  subroutine unique_digits(x_len, x, result)
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
+    integer, intent(in) :: x(*)
+    integer, allocatable, intent(out) :: result(:)
+    integer :: i, n, temp
+    integer :: digits(10)
+    integer :: num, digit
+
+    n = 0
+    do i = 1, x_len
+      num = x(i)
+      digits = 0
+      do while (num > 0)
+        digit = mod(num, 10)
+        if (mod(digit, 2) == 0) then
+          digits(digit) = 1
         end if
+        num = num / 10
+      end do
+      if (sum(digits) == 0) then
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
+    n = 0
+    do i = 1, x_len
+      num = x(i)
+      digits = 0
+      do while (num > 0)
+        digit = mod(num, 10)
+        if (mod(digit, 2) == 0) then
+          digits(digit) = 1
         end if
+        num = num / 10
+      end do
+      if (sum(digits) == 0) then
+        n = n + 1
+        result(n) = x(i)
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
+    call sort(result, n)
+  end subroutine unique_digits
+
+  subroutine sort(arr, n)
+    implicit none
+    integer, intent(inout) :: arr(*)
+    integer, intent(in) :: n
+    integer :: i, j, temp
+    do i = 1, n-1
+      do j = i+1, n
+        if (arr(j) < arr(i)) then
+          temp = arr(i)
+          arr(i) = arr(j)
+          arr(j) = temp
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
+  end subroutine sort
+
+end program unique_digits_demo
```
