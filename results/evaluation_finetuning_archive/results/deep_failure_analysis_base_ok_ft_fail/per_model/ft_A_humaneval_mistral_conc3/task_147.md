# Failure case: ft_A_humaneval_mistral_conc3 / task 147

- Base status: `ok`

- FT status: `compile_err`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_stdin_read, status_compile_err`


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
  "num_lines": {
    "base": 39,
    "ft": 30
  },
  "num_nonempty_lines": {
    "base": 32,
    "ft": 25
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
program main
  implicit none
  integer :: n
  integer, allocatable :: a(:)
  integer :: count

  ! Read input n
  read(*,*) n

  ! Create array a
  allocate(a(n))
  a = [(i*i - i + 1, i = 1, n)]

  ! Count triples with sum divisible by 3
  count = 0
  do k = 3, n
    do j = 2, k-1
      do i = 1, j-1
        if (mod(a(i) + a(j) + a(k), 3) == 0) then
          count = count + 1
        end if
      end do
    end do
  end do

  ! Output result
  print *, count

  deallocate(a)
end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,39 +1,30 @@
-program count_triples
-    implicit none
-    integer :: n
-    integer, allocatable :: a(:)
-    integer :: i, j, k
-    integer :: count
-    integer :: sum_val
+program main
+  implicit none
+  integer :: n
+  integer, allocatable :: a(:)
+  integer :: count
 
-    ! Read input
-    read *, n
+  ! Read input n
+  read(*,*) n
 
-    ! Allocate array
-    allocate(a(n))
+  ! Create array a
+  allocate(a(n))
+  a = [(i*i - i + 1, i = 1, n)]
 
-    ! Fill array with a[i] = i*i - i + 1
-    do i = 1, n
-        a(i) = i*i - i + 1
+  ! Count triples with sum divisible by 3
+  count = 0
+  do k = 3, n
+    do j = 2, k-1
+      do i = 1, j-1
+        if (mod(a(i) + a(j) + a(k), 3) == 0) then
+          count = count + 1
+        end if
+      end do
     end do
+  end do
 
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
+  ! Output result
+  print *, count
 
-    ! Output result
-    write (*, *) count
-
-    ! Deallocate
-    deallocate(a)
-
-end program count_triples
+  deallocate(a)
+end program main
```
