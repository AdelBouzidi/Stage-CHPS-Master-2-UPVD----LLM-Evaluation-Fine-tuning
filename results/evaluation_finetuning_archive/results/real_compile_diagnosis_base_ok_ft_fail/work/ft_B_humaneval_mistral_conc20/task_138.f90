program is_equal_to_sum_even
    implicit none
    integer :: n
    logical :: result
    
    read *, n
    
    if (n >= 8 .and. mod(n, 2) == 0) then
        result = .true.
    else
        result = .false.
    end if
    
    print *, result
end program is_equal_to_sum_even