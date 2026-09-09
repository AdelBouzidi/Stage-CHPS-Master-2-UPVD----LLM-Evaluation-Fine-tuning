program starts_one_ends
    implicit none
    integer :: n
    integer :: result

    ! Read input from stdin
    read(*,*) n

    ! Calculate result
    result = starts_one_ends(n)

    ! Print result to stdout
    print *, result

contains

    function starts_one_ends(n) result(res)
        implicit none
        integer, intent(in) :: n
        integer :: res
        if (n == 1) then
            res = 1
        else
            res = 9 * 10**(n-1) + 10**(n-1) - 10**(n-2)
        end if
    end function starts_one_ends

end program starts_one_ends