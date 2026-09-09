# Failure case: ft_A_half2_humaneval_mistral_conc20 / task 104

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
    "ft": 54
  },
  "num_nonempty_lines": {
    "base": 61,
    "ft": 47
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
  integer :: result(max_len)
  integer :: n
  integer :: i, j, k
  logical :: has_even_digit

  ! Read input
  read(*,*) x_len
  read(*,*) (x(i), i=1,x_len)

  ! Initialize result array
  n = 0
  do i = 1, x_len
    if (.not. has_even_digit(x(i))) then
      n = n + 1
      result(n) = x(i)
    end if
  end do

  ! Sort result array (simple bubble sort)
  do i = 1, n-1
    do j = i+1, n
      if (result(i) > result(j)) then
        k = result(i)
        result(i) = result(j)
        result(j) = k
      end if
    end do
  end do

  ! Output result
  write(*,*) (result(i), i=1,n)

contains

  logical function has_even_digit(num)
    integer, intent(in) :: num
    integer :: temp
    temp = abs(num)
    do while (temp > 0)
      if (mod(temp, 10) == 0 .or. mod(temp, 10) == 2 .or. mod(temp, 10) == 4 .or. mod(temp, 10) == 6 .or. mod(temp, 10) == 8) then
        has_even_digit = .true.
        return
      end if
      temp = temp / 10
    end do
    has_even_digit = .false.
  end function has_even_digit

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,73 +1,54 @@
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
+program main
+  implicit none
+  integer, parameter :: max_len = 100
+  integer :: x_len
+  integer :: x(max_len)
+  integer :: result(max_len)
+  integer :: n
+  integer :: i, j, k
+  logical :: has_even_digit
+
+  ! Read input
+  read(*,*) x_len
+  read(*,*) (x(i), i=1,x_len)
+
+  ! Initialize result array
+  n = 0
+  do i = 1, x_len
+    if (.not. has_even_digit(x(i))) then
+      n = n + 1
+      result(n) = x(i)
+    end if
+  end do
+
+  ! Sort result array (simple bubble sort)
+  do i = 1, n-1
+    do j = i+1, n
+      if (result(i) > result(j)) then
+        k = result(i)
+        result(i) = result(j)
+        result(j) = k
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
-        end if
+  end do
+
+  ! Output result
+  write(*,*) (result(i), i=1,n)
+
+contains
+
+  logical function has_even_digit(num)
+    integer, intent(in) :: num
+    integer :: temp
+    temp = abs(num)
+    do while (temp > 0)
+      if (mod(temp, 10) == 0 .or. mod(temp, 10) == 2 .or. mod(temp, 10) == 4 .or. mod(temp, 10) == 6 .or. mod(temp, 10) == 8) then
+        has_even_digit = .true.
+        return
+      end if
+      temp = temp / 10
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
+    has_even_digit = .false.
+  end function has_even_digit
+
+end program main
```
