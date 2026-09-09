program is_simple_power
    implicit none
    integer :: x, n
    integer :: result
    
    ! Read input
    read *, x
    read *, n
    
    ! Check if x is a simple power of n
    if (n == 0) then
        if (x == 0) then
            result = .true.
        else
            result = .false.
        end if
    else if (n == 1) then
        if (x == 1) then
            result = .true.
        else
            result = .false.
        end if
    else if (x == 1) then
        result = .true.
    else if (x < 0) then
        if (n < 0) then
            ! Check if x is a power of n with even exponent
            result = .false.
        else
            result = .false.
        end if
    else
        ! x > 0 and n > 0
        result = .false.
        do while (x > 1)
            if (mod(x, n) /= 0) exit
            x = x / n
        end do
        if (x == 1) then
            result = .true.
        end if
    end if
    
    ! Output result
    print *, result
end program is_simple_power