# Failure case: ft_ABC_source_stack_v1_humaneval_mistral_conc20 / task 150

- Base status: `ok`

- FT status: `ok`

- Primary cause: `status_ok`

- Labels: `status_ok`


## Prompt

```text
Write a Fortran90 program that returns the value of x if n is a prime number and returns the value of y otherwise.
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
{}
```


## Base generated code

```fortran
program x_or_y
    implicit none
    integer :: n, x, y
    integer :: i
    logical :: is_prime
    
    ! Read input
    read *, n
    read *, x
    read *, y
    
    ! Check if n is prime
    is_prime = .true.
    if (n <= 1) then
        is_prime = .false.
    else
        do i = 2, int(sqrt(real(n)))
            if (mod(n, i) == 0) then
                is_prime = .false.
                exit
            end if
        end do
    end if
    
    ! Output result
    if (is_prime) then
        print *, x
    else
        print *, y
    end if
    
end program x_or_y
```


## FT generated code

```fortran
program main
  implicit none
  integer :: n, x, y
  integer :: i
  logical :: is_prime

  ! Read input
  read *, n
  read *, x
  read *, y

  ! Check if n is prime
  is_prime = .true.
  if (n <= 1) then
    is_prime = .false.
  else
    do i = 2, n - 1
      if (mod(n, i) == 0) then
        is_prime = .false.
        exit
      end if
    end do
  end if

  ! Output result
  if (is_prime) then
    print *, x
  else
    print *, y
  end if

end program main
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,32 +1,32 @@
-program x_or_y
-    implicit none
-    integer :: n, x, y
-    integer :: i
-    logical :: is_prime
-    
-    ! Read input
-    read *, n
-    read *, x
-    read *, y
-    
-    ! Check if n is prime
-    is_prime = .true.
-    if (n <= 1) then
+program main
+  implicit none
+  integer :: n, x, y
+  integer :: i
+  logical :: is_prime
+
+  ! Read input
+  read *, n
+  read *, x
+  read *, y
+
+  ! Check if n is prime
+  is_prime = .true.
+  if (n <= 1) then
+    is_prime = .false.
+  else
+    do i = 2, n - 1
+      if (mod(n, i) == 0) then
         is_prime = .false.
-    else
-        do i = 2, int(sqrt(real(n)))
-            if (mod(n, i) == 0) then
-                is_prime = .false.
-                exit
-            end if
-        end do
-    end if
-    
-    ! Output result
-    if (is_prime) then
-        print *, x
-    else
-        print *, y
-    end if
-    
-end program x_or_y
+        exit
+      end if
+    end do
+  end if
+
+  ! Output result
+  if (is_prime) then
+    print *, x
+  else
+    print *, y
+  end if
+
+end program main
```
