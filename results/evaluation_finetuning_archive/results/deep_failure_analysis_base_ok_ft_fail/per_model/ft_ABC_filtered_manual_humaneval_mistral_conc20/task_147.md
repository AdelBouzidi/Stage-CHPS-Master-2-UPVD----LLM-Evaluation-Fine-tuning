# Failure case: ft_ABC_filtered_manual_humaneval_mistral_conc20 / task 147

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `status_compile_err`

- Labels: `status_compile_err`


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
  "has_program": {
    "base": true,
    "ft": false
  },
  "num_lines": {
    "base": 39,
    "ft": 0
  },
  "num_nonempty_lines": {
    "base": 32,
    "ft": 0
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
  "uses_hardcoded_scalars": {
    "base": true,
    "ft": false
  },
  "uses_implicit_none": {
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

```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,39 +0,0 @@
-program count_triples
-    implicit none
-    integer :: n
-    integer, allocatable :: a(:)
-    integer :: i, j, k
-    integer :: count
-    integer :: sum_val
-
-    ! Read input
-    read *, n
-
-    ! Allocate array
-    allocate(a(n))
-
-    ! Fill array with a[i] = i*i - i + 1
-    do i = 1, n
-        a(i) = i*i - i + 1
-    end do
-
-    ! Count triples where sum is multiple of 3
-    count = 0
-    do i = 1, n-2
-        do j = i+1, n-1
-            do k = j+1, n
-                sum_val = a(i) + a(j) + a(k)
-                if (mod(sum_val, 3) == 0) then
-                    count = count + 1
-                end if
-            end do
-        end do
-    end do
-
-    ! Output result
-    write (*, *) count
-
-    ! Deallocate
-    deallocate(a)
-
-end program count_triples
```
