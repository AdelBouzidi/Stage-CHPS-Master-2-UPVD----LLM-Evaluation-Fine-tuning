# Failure case: ft_ABC_source_fortran_lang_humaneval_mistral_conc20 / task 106

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_output_labels, status_ok`


## Prompt

```text
Write a Fortran90 program that, given a positive integer n, returns an array of size n where the value of the element at index i (starting from 1) is the factorial of i if i is even, and the sum of numbers from 1 to i if i is odd.
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
    "base": 34,
    "ft": 35
  },
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program factorial_sum_array
    implicit none
    integer :: n, i, j
    integer, allocatable :: result(:)
    integer :: factorial, sum_val

    ! Read input
    read *, n

    ! Allocate array
    allocate(result(n))

    ! Compute values
    do i = 1, n
        if (mod(i, 2) == 0) then
            ! Even index: factorial of i
            factorial = 1
            do j = 1, i
                factorial = factorial * j
            end do
            result(i) = factorial
        else
            ! Odd index: sum from 1 to i
            sum_val = i * (i + 1) / 2
            result(i) = sum_val
        end if
    end do

    ! Output result
    do i = 1, n
        write (*, '(I0)') result(i)
    end do

end program factorial_sum_array
```


## FT generated code

```fortran
program factorial_sum_array
    implicit none
    integer :: n, i, j
    integer, allocatable :: result(:)
    
    ! Read input
    read *, n
    
    ! Allocate array
    allocate(result(n))
    
    ! Compute values
    do i = 1, n
        if (mod(i, 2) == 0) then
            ! Even: factorial
            result(i) = 1
            do j = 1, i
                result(i) = result(i) * j
            end do
        else
            ! Odd: sum from 1 to i
            result(i) = i * (i + 1) / 2
        end if
    end do
    
    ! Output
    do i = 1, n
        write (*, '(I0)') result(i)
        if (i < n) write (*, '(A)') ' '
    end do
    
    ! Clean up
    deallocate(result)
    
end program factorial_sum_array
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -2,33 +2,34 @@
     implicit none
     integer :: n, i, j
     integer, allocatable :: result(:)
-    integer :: factorial, sum_val
-
+    
     ! Read input
     read *, n
-
+    
     ! Allocate array
     allocate(result(n))
-
+    
     ! Compute values
     do i = 1, n
         if (mod(i, 2) == 0) then
-            ! Even index: factorial of i
-            factorial = 1
+            ! Even: factorial
+            result(i) = 1
             do j = 1, i
-                factorial = factorial * j
+                result(i) = result(i) * j
             end do
-            result(i) = factorial
         else
-            ! Odd index: sum from 1 to i
-            sum_val = i * (i + 1) / 2
-            result(i) = sum_val
+            ! Odd: sum from 1 to i
+            result(i) = i * (i + 1) / 2
         end if
     end do
-
-    ! Output result
+    
+    ! Output
     do i = 1, n
         write (*, '(I0)') result(i)
+        if (i < n) write (*, '(A)') ' '
     end do
-
+    
+    ! Clean up
+    deallocate(result)
+    
 end program factorial_sum_array
```
