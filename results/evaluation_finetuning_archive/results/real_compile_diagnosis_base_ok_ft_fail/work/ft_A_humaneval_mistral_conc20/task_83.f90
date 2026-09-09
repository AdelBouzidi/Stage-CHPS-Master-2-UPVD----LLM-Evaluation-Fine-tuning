program starts_one_ends_demo
    implicit none
    integer :: n
    integer :: result

    ! Hardcoded input value
    n = 1

    ! Call the function
    result = starts_one_ends(n)

    ! Output the result
    print *, 'starts_one_ends(', n, ') =', result

contains

    integer function starts_one_ends(n)
        integer, intent(in) :: n
        if (n == 1) then
            starts_one_ends = 1
        else
            starts_one_ends = 10**(n-1) + 9*10**(n-2) - 10**(n-2)
        end if
    end function starts_one_ends

end program starts_one_ends_demo