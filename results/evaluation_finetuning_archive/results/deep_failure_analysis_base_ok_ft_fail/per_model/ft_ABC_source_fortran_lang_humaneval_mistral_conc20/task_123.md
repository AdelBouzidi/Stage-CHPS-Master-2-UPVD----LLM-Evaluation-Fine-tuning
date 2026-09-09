# Failure case: ft_ABC_source_fortran_lang_humaneval_mistral_conc20 / task 123

- Base status: `ok`

- FT status: `runtime_err`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, status_runtime_err`


## Prompt

```text
Write a Fortran90 program that returns a sorted array containing the odd numbers present in the Collatz sequence of a given positive integer.
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
    "base": 60,
    "ft": 44
  },
  "num_nonempty_lines": {
    "base": 53,
    "ft": 38
  },
  "uses_allocate": {
    "base": true,
    "ft": false
  }
}
```


## Base generated code

```fortran
program collatz_odds
    implicit none
    integer :: n
    integer, allocatable :: odd_collatz(:)
    integer :: i, j, temp, count

    ! Read input
    read *, n

    ! Collect odd numbers from Collatz sequence
    count = 0
    temp = n
    do while (temp > 0)
        if (mod(temp, 2) == 1) then
            count = count + 1
        end if
        if (temp == 1) exit
        if (mod(temp, 2) == 0) then
            temp = temp / 2
        else
            temp = 3 * temp + 1
        end if
    end do

    ! Allocate array for odd numbers
    allocate(odd_collatz(count))
    count = 0

    ! Collect odd numbers again
    temp = n
    do while (temp > 0)
        if (mod(temp, 2) == 1) then
            count = count + 1
            odd_collatz(count) = temp
        end if
        if (temp == 1) exit
        if (mod(temp, 2) == 0) then
            temp = temp / 2
        else
            temp = 3 * temp + 1
        end if
    end do

    ! Sort the odd numbers using bubble sort
    do i = 1, count - 1
        do j = i + 1, count
            if (odd_collatz(i) > odd_collatz(j)) then
                odd_collatz(i) = odd_collatz(i) + odd_collatz(j)
                odd_collatz(j) = odd_collatz(i) - odd_collatz(j)
                odd_collatz(i) = odd_collatz(i) - odd_collatz(j)
            end if
        end do
    end do

    ! Output the sorted odd numbers
    do i = 1, count
        write (*, '(I0)') odd_collatz(i)
    end do

end program collatz_odds
```


## FT generated code

```fortran
program collatz_odds
    implicit none
    integer :: n
    integer, allocatable :: odd_collatz(:)
    integer :: i, j, temp
    integer :: count
    
    ! Read input
    read *, n
    
    ! Generate Collatz sequence and collect odd numbers
    odd_collatz = 0
    count = 0
    
    do
        if (mod(n, 2) == 1) then
            count = count + 1
            odd_collatz(count) = n
        end if
        if (n == 1) exit
        if (mod(n, 2) == 0) then
            n = n / 2
        else
            n = 3 * n + 1
        end if
    end do
    
    ! Sort the odd numbers
    do i = 1, count - 1
        do j = i + 1, count
            if (odd_collatz(i) > odd_collatz(j)) then
                temp = odd_collatz(i)
                odd_collatz(i) = odd_collatz(j)
                odd_collatz(j) = temp
            end if
        end do
    end do
    
    ! Output the sorted odd numbers
    do i = 1, count
        write (*, '(I0)') odd_collatz(i)
    end do
    
end program collatz_odds
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -2,59 +2,43 @@
     implicit none
     integer :: n
     integer, allocatable :: odd_collatz(:)
-    integer :: i, j, temp, count
-
+    integer :: i, j, temp
+    integer :: count
+    
     ! Read input
     read *, n
-
-    ! Collect odd numbers from Collatz sequence
+    
+    ! Generate Collatz sequence and collect odd numbers
+    odd_collatz = 0
     count = 0
-    temp = n
-    do while (temp > 0)
-        if (mod(temp, 2) == 1) then
+    
+    do
+        if (mod(n, 2) == 1) then
             count = count + 1
+            odd_collatz(count) = n
         end if
-        if (temp == 1) exit
-        if (mod(temp, 2) == 0) then
-            temp = temp / 2
+        if (n == 1) exit
+        if (mod(n, 2) == 0) then
+            n = n / 2
         else
-            temp = 3 * temp + 1
+            n = 3 * n + 1
         end if
     end do
-
-    ! Allocate array for odd numbers
-    allocate(odd_collatz(count))
-    count = 0
-
-    ! Collect odd numbers again
-    temp = n
-    do while (temp > 0)
-        if (mod(temp, 2) == 1) then
-            count = count + 1
-            odd_collatz(count) = temp
-        end if
-        if (temp == 1) exit
-        if (mod(temp, 2) == 0) then
-            temp = temp / 2
-        else
-            temp = 3 * temp + 1
-        end if
-    end do
-
-    ! Sort the odd numbers using bubble sort
+    
+    ! Sort the odd numbers
     do i = 1, count - 1
         do j = i + 1, count
             if (odd_collatz(i) > odd_collatz(j)) then
-                odd_collatz(i) = odd_collatz(i) + odd_collatz(j)
-                odd_collatz(j) = odd_collatz(i) - odd_collatz(j)
-                odd_collatz(i) = odd_collatz(i) - odd_collatz(j)
+                temp = odd_collatz(i)
+                odd_collatz(i) = odd_collatz(j)
+                odd_collatz(j) = temp
             end if
         end do
     end do
-
+    
     ! Output the sorted odd numbers
     do i = 1, count
         write (*, '(I0)') odd_collatz(i)
     end do
-
+    
 end program collatz_odds
```
