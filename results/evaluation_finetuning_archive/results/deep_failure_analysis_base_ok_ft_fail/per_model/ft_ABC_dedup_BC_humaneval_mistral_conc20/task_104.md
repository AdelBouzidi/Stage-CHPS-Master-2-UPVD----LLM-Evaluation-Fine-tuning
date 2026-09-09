# Failure case: ft_ABC_dedup_BC_humaneval_mistral_conc20 / task 104

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
    "ft": 56
  },
  "num_nonempty_lines": {
    "base": 61,
    "ft": 48
  },
  "uses_allocatable": {
    "base": true,
    "ft": false
  },
  "uses_allocate": {
    "base": true,
    "ft": false
  },
  "uses_assumed_shape": {
    "base": true,
    "ft": false
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
  integer, parameter :: max_len = 100
  integer :: x_len
  integer :: x(max_len)
  integer :: y(max_len)
  integer :: y_len
  integer :: i, j, k
  integer :: temp

  ! Read input
  read(*,*) x_len
  read(*,*) (x(i), i=1,x_len)

  ! Initialize y_len
  y_len = 0

  ! Process each element
  do i = 1, x_len
    if (contains_even_digit(x(i))) then
      y_len = y_len + 1
      y(y_len) = x(i)
    end if
  end do

  ! Sort y array
  do i = 1, y_len
    do j = i+1, y_len
      if (y(i) > y(j)) then
        temp = y(i)
        y(i) = y(j)
        y(j) = temp
      end if
    end do
  end do

  ! Output result
  print *, (y(i), i=1,y_len)

contains

  logical function contains_even_digit(n)
    integer, intent(in) :: n
    integer :: digit
    contains_even_digit = .false.
    do while (n > 0)
      digit = mod(n, 10)
      if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
        contains_even_digit = .true.
        return
      end if
      n = n / 10
    end do
  end function contains_even_digit

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,73 +1,56 @@
-program filter_odd_digits
-    implicit none
-    integer, parameter :: max_len = 1000
-    integer :: n, i, j, temp
-    integer, allocatable :: x(:), result(:)
-    integer :: len_result
+program main
+  implicit none
+  integer, parameter :: max_len = 100
+  integer :: x_len
+  integer :: x(max_len)
+  integer :: y(max_len)
+  integer :: y_len
+  integer :: i, j, k
+  integer :: temp
+
+  ! Read input
+  read(*,*) x_len
+  read(*,*) (x(i), i=1,x_len)
+
+  ! Initialize y_len
+  y_len = 0
+
+  ! Process each element
+  do i = 1, x_len
+    if (contains_even_digit(x(i))) then
+      y_len = y_len + 1
+      y(y_len) = x(i)
+    end if
+  end do
+
+  ! Sort y array
+  do i = 1, y_len
+    do j = i+1, y_len
+      if (y(i) > y(j)) then
+        temp = y(i)
+        y(i) = y(j)
+        y(j) = temp
+      end if
+    end do
+  end do
+
+  ! Output result
+  print *, (y(i), i=1,y_len)
+
+contains
+
+  logical function contains_even_digit(n)
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
+    contains_even_digit = .false.
+    do while (n > 0)
+      digit = mod(n, 10)
+      if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
+        contains_even_digit = .true.
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
+  end function contains_even_digit
+
+end program main
```
