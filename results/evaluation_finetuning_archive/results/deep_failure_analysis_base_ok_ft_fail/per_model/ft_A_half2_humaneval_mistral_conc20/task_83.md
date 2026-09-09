# Failure case: ft_A_half2_humaneval_mistral_conc20 / task 83

- Base status: `ok`

- FT status: `ineq`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ineq`


## Prompt

```text
Write a Fortran90 program that returns the count of n-digit positive integers that start or end with 1.
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
    "base": 16,
    "ft": 14
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
program count_start_or_end_one
    implicit none
    integer :: n
    integer :: result

    read(*,*) n

    if (n == 1) then
        result = 1
    else
        result = 18 * 10**(n - 2)
    end if

    write(*,*) result

end program count_start_or_end_one
```


## FT generated code

```fortran
program starts_one_ends
    implicit none
    integer :: n
    integer :: result

    read(*,*) n
    if (n == 1) then
        result = 1
    else
        result = 19 * 10**(n-2)
    end if

    print *, result
end program starts_one_ends
```


## Unified diff base vs FT

```diff
--- base_code
+++ ft_code
@@ -1,16 +1,14 @@
-program count_start_or_end_one
+program starts_one_ends
     implicit none
     integer :: n
     integer :: result
 
     read(*,*) n
-
     if (n == 1) then
         result = 1
     else
-        result = 18 * 10**(n - 2)
+        result = 19 * 10**(n-2)
     end if
 
-    write(*,*) result
-
-end program count_start_or_end_one
+    print *, result
+end program starts_one_ends
```
