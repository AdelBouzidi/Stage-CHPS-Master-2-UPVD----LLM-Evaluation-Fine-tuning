# Failure case: ft_A_humaneval_mistral_conc20 / task 147

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `status_ineq`

- Labels: `status_ineq`


## Prompt

```text
Write a Fortran90 program that takes a positive integer n, constructs an integer array a of length n where a[i] = i*i - i + 1, and returns the number of triples (a[i], a[j], a[k]) with i < j < k such that their sum is a multiple of 3.
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
    "base": false,
    "ft": true
  },
  "num_lines": {
    "base": 39,
    "ft": 28
  },
  "num_nonempty_lines": {
    "base": 32,
    "ft": 24
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
program count_triples
    implicit none
    integer :: n
    integer, allocatable :: a(:)
    integer :: i, j, k
    integer :: count
    integer :: sum_val

    ! Read input
    read *, n

    ! Allocate array
    allocate(a(n))

    ! Fill array with a[i] = i*i - i + 1
    do i = 1, n
        a(i) = i*i - i + 1
    end do

    ! Count triples where sum is multiple of 3
    count = 0
    do i = 1, n-2
        do j = i+1, n-1
            do k = j+1, n
                sum_val = a(i) + a(j) + a(k)
                if (mod(sum_val, 3) == 0) then
                    count = count + 1
                end if
            end do
        end do
    end do

    ! Output result
    write (*, *) count

    ! Deallocate
    deallocate(a)

end program count_triples
```


## FT generated code

```fortran
program get_max_triples
    implicit none
    integer, parameter :: n = 5
    integer :: a(n)
    integer :: i, j, k, count
    integer :: result

    ! Initialize array a with a[i] = i*i - i + 1
    do i = 1, n
        a(i) = i*i - i + 1
    end do

    ! Count triples (i, j, k) with i < j < k where sum is divisible by 3
    count = 0
    do i = 1, n-2
        do j = i+1, n-1
            do k = j+1, n
                if (mod(a(i) + a(j) + a(k), 3) == 0) then
                    count = count + 1
                end if
            end do
        end do
    end do

    result = count
    print *, result

end program get_max_triples
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,39 +1,28 @@
-program count_triples
+program get_max_triples
     implicit none
-    integer :: n
-    integer, allocatable :: a(:)
-    integer :: i, j, k
-    integer :: count
-    integer :: sum_val
+    integer, parameter :: n = 5
+    integer :: a(n)
+    integer :: i, j, k, count
+    integer :: result
 
-    ! Read input
-    read *, n
-
-    ! Allocate array
-    allocate(a(n))
-
-    ! Fill array with a[i] = i*i - i + 1
+    ! Initialize array a with a[i] = i*i - i + 1
     do i = 1, n
         a(i) = i*i - i + 1
     end do
 
-    ! Count triples where sum is multiple of 3
+    ! Count triples (i, j, k) with i < j < k where sum is divisible by 3
     count = 0
     do i = 1, n-2
         do j = i+1, n-1
             do k = j+1, n
-                sum_val = a(i) + a(j) + a(k)
-                if (mod(sum_val, 3) == 0) then
+                if (mod(a(i) + a(j) + a(k), 3) == 0) then
                     count = count + 1
                 end if
             end do
         end do
     end do
 
-    ! Output result
-    write (*, *) count
+    result = count
+    print *, result
 
-    ! Deallocate
-    deallocate(a)
-
-end program count_triples
+end program get_max_triples
```
