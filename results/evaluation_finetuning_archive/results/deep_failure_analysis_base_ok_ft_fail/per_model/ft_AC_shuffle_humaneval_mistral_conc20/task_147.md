# Failure case: ft_AC_shuffle_humaneval_mistral_conc20 / task 147

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_assumed_shape_needs_interface`

- Labels: `static_assumed_shape_needs_interface, static_stdin_read, status_ok`


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
    "ft": 36
  },
  "num_nonempty_lines": {
    "base": 32,
    "ft": 29
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
program get_max_triples
  implicit none
  integer :: n
  integer, allocatable :: a(:)
  integer :: i, j, k, count

  ! Read input
  read(*,*) n

  ! Allocate array
  allocate(a(n))

  ! Fill array with values
  do i = 1, n
    a(i) = i*i - i + 1
  end do

  ! Count triples
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

  ! Output result
  print *, count

  ! Clean up
  deallocate(a)

end program get_max_triples
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,39 +1,36 @@
-program count_triples
-    implicit none
-    integer :: n
-    integer, allocatable :: a(:)
-    integer :: i, j, k
-    integer :: count
-    integer :: sum_val
+program get_max_triples
+  implicit none
+  integer :: n
+  integer, allocatable :: a(:)
+  integer :: i, j, k, count
 
-    ! Read input
-    read *, n
+  ! Read input
+  read(*,*) n
 
-    ! Allocate array
-    allocate(a(n))
+  ! Allocate array
+  allocate(a(n))
 
-    ! Fill array with a[i] = i*i - i + 1
-    do i = 1, n
-        a(i) = i*i - i + 1
+  ! Fill array with values
+  do i = 1, n
+    a(i) = i*i - i + 1
+  end do
+
+  ! Count triples
+  count = 0
+  do i = 1, n-2
+    do j = i+1, n-1
+      do k = j+1, n
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
+  ! Clean up
+  deallocate(a)
 
-    ! Deallocate
-    deallocate(a)
-
-end program count_triples
+end program get_max_triples
```
