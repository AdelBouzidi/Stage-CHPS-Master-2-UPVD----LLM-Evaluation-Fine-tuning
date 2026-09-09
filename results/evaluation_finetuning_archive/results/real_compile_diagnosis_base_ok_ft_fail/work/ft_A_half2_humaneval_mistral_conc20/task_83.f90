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