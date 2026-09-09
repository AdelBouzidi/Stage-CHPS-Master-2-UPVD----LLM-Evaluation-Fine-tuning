# Failure case: ft_ABC_source_stack_v1_humaneval_mistral_conc20 / task 104

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
    "ft": 60
  },
  "num_nonempty_lines": {
    "base": 61,
    "ft": 51
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
  integer, allocatable :: x(:)
  integer :: n, i, j, temp
  integer :: filtered_count
  integer, allocatable :: filtered(:)
  integer :: digit

  ! Read array length
  read(*,*) n

  ! Read array elements
  allocate(x(n))
  read(*,*) x

  ! Filter elements that don't contain any even digit
  filtered_count = 0
  allocate(filtered(n))
  do i = 1, n
    if (has_odd_digits_only(x(i))) then
      filtered_count = filtered_count + 1
      filtered(filtered_count) = x(i)
    end if
  end do

  ! Sort filtered array
  do i = 1, filtered_count - 1
    do j = i + 1, filtered_count
      if (filtered(i) > filtered(j)) then
        temp = filtered(i)
        filtered(i) = filtered(j)
        filtered(j) = temp
      end if
    end do
  end do

  ! Output filtered array
  do i = 1, filtered_count
    if (i > 1) print *, ' '
    print *, filtered(i)
  end do

contains

  logical function has_odd_digits_only(num)
    integer, intent(in) :: num
    integer :: digit

    has_odd_digits_only = .true.
    do while (num > 0)
      digit = mod(num, 10)
      if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
        has_odd_digits_only = .false.
        return
      end if
      num = num / 10
    end do
  end function has_odd_digits_only

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,73 +1,60 @@
-program filter_odd_digits
-    implicit none
-    integer, parameter :: max_len = 1000
-    integer :: n, i, j, temp
-    integer, allocatable :: x(:), result(:)
-    integer :: len_result
+program main
+  implicit none
+  integer, allocatable :: x(:)
+  integer :: n, i, j, temp
+  integer :: filtered_count
+  integer, allocatable :: filtered(:)
+  integer :: digit
+
+  ! Read array length
+  read(*,*) n
+
+  ! Read array elements
+  allocate(x(n))
+  read(*,*) x
+
+  ! Filter elements that don't contain any even digit
+  filtered_count = 0
+  allocate(filtered(n))
+  do i = 1, n
+    if (has_odd_digits_only(x(i))) then
+      filtered_count = filtered_count + 1
+      filtered(filtered_count) = x(i)
+    end if
+  end do
+
+  ! Sort filtered array
+  do i = 1, filtered_count - 1
+    do j = i + 1, filtered_count
+      if (filtered(i) > filtered(j)) then
+        temp = filtered(i)
+        filtered(i) = filtered(j)
+        filtered(j) = temp
+      end if
+    end do
+  end do
+
+  ! Output filtered array
+  do i = 1, filtered_count
+    if (i > 1) print *, ' '
+    print *, filtered(i)
+  end do
+
+contains
+
+  logical function has_odd_digits_only(num)
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
-        end if
+
+    has_odd_digits_only = .true.
+    do while (num > 0)
+      digit = mod(num, 10)
+      if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
+        has_odd_digits_only = .false.
+        return
+      end if
+      num = num / 10
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
+  end function has_odd_digits_only
+
+end program main
```
