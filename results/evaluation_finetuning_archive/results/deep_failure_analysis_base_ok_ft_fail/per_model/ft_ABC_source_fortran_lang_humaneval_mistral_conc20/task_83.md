# Failure case: ft_ABC_source_fortran_lang_humaneval_mistral_conc20 / task 83

- Base status: `ok`

- FT status: `ok`

- Primary cause: `static_stdin_read`

- Labels: `static_stdin_read, status_ok`


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
{}
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


## Unified diff base vs FT

```diff

```
