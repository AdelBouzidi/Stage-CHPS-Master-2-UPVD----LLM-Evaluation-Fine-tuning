program starts_one_ends
    implicit none
    integer :: n
    integer :: result

    ! Read input from stdin
    read(*,*) n

    ! Calculate the result
    if (n == 1) then
        result = 1
    else
        result = 18 * 10**(n-2)
    end if

    ! Print the result to stdout
    print *, result

end program starts_one_ends