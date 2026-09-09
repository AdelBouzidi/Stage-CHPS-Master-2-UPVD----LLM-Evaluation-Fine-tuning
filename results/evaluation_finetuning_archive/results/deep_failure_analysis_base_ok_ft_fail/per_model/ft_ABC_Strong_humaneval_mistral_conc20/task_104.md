# Failure case: ft_ABC_Strong_humaneval_mistral_conc20 / task 104

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_output_labels`

- Labels: `static_modifies_intent_in_possible, static_output_labels, status_compile_err`


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
  "num_lines": {
    "base": 73,
    "ft": 75
  },
  "num_nonempty_lines": {
    "base": 61,
    "ft": 64
  },
  "num_subroutines": {
    "base": 0,
    "ft": 1
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
  integer, parameter :: dp = kind(1.0d0)
  integer :: x_len
  integer, allocatable :: x(:)
  integer, allocatable :: result(:)
  integer :: i

  ! Hardcoded test case from the example
  x_len = 4
  allocate(x(x_len))
  x = [15, 33, 1422, 1]

  call unique_digits(x_len, x, result)

  print *, 'Result:', result

contains

  subroutine unique_digits(x_len, x, result)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(x_len)
    integer, allocatable, intent(out) :: result(:)
    integer :: i, j, k, n
    integer :: temp
    integer :: digit
    logical :: contains_even_digit

    ! Count how many elements pass the filter
    n = 0
    do i = 1, x_len
      if (.not. contains_even_digit(x(i))) then
        n = n + 1
      end if
    end do

    allocate(result(n))
    k = 0
    do i = 1, x_len
      if (.not. contains_even_digit(x(i))) then
        k = k + 1
        result(k) = x(i)
      end if
    end do

    ! Sort the result array in increasing order
    do i = 1, n - 1
      do j = i + 1, n
        if (result(i) > result(j)) then
          temp = result(i)
          result(i) = result(j)
          result(j) = temp
        end if
      end do
    end do

  end subroutine unique_digits

  logical function contains_even_digit(val)
    implicit none
    integer, intent(in) :: val
    integer :: temp, digit
    contains_even_digit = .false.
    do while (val > 0)
      digit = mod(val, 10)
      if (mod(digit, 2) == 0) then
        contains_even_digit = .true.
        return
      end if
      val = val / 10
    end do
  end function contains_even_digit

end program unique_digits_demo
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,73 +1,75 @@
-program filter_odd_digits
+program unique_digits_demo
+  implicit none
+  integer, parameter :: dp = kind(1.0d0)
+  integer :: x_len
+  integer, allocatable :: x(:)
+  integer, allocatable :: result(:)
+  integer :: i
+
+  ! Hardcoded test case from the example
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
+    integer, intent(in) :: x_len
+    integer, intent(in) :: x(x_len)
+    integer, allocatable, intent(out) :: result(:)
+    integer :: i, j, k, n
+    integer :: temp
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
+    logical :: contains_even_digit
+
+    ! Count how many elements pass the filter
+    n = 0
+    do i = 1, x_len
+      if (.not. contains_even_digit(x(i))) then
+        n = n + 1
+      end if
+    end do
+
+    allocate(result(n))
+    k = 0
+    do i = 1, x_len
+      if (.not. contains_even_digit(x(i))) then
+        k = k + 1
+        result(k) = x(i)
+      end if
+    end do
+
+    ! Sort the result array in increasing order
+    do i = 1, n - 1
+      do j = i + 1, n
+        if (result(i) > result(j)) then
+          temp = result(i)
+          result(i) = result(j)
+          result(j) = temp
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
+
+  end subroutine unique_digits
+
+  logical function contains_even_digit(val)
+    implicit none
+    integer, intent(in) :: val
+    integer :: temp, digit
+    contains_even_digit = .false.
+    do while (val > 0)
+      digit = mod(val, 10)
+      if (mod(digit, 2) == 0) then
+        contains_even_digit = .true.
+        return
+      end if
+      val = val / 10
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
+  end function contains_even_digit
+
+end program unique_digits_demo
```
