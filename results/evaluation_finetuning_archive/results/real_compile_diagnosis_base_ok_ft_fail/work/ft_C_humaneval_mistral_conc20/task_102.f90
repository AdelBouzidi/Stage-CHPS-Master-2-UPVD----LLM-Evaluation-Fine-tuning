program choose_num
    implicit none
    integer :: x, y, result

    ! Read input
    read(*, *) x
    read(*, *) y

    ! Find the largest even number in range [x, y]
    if (y < x) then
        result = -1
    else if (mod(y, 2) == 0) then
        result = y
    else
        result = y - 1
    end if

    ! Output result
    print *, result
end program choose_num