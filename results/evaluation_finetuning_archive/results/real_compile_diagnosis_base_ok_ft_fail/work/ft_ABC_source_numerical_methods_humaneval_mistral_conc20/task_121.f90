program sum_odd_at_even_positions
    implicit none
    integer :: n
    integer, allocatable :: lst(:)
    integer :: i
    integer :: sum = 0
    
    ! Read array length
    read *, n
    
    ! Allocate array
    allocate(lst(n))
    
    ! Read array elements
    read *, lst
    
    ! Calculate sum of odd elements at even positions (0-indexed)
    sum = 0
    do i = 0, n-1
        if (mod(i, 2) == 0) then
            if (mod(lst(i+1), 2) /= 0) then
                sum = sum + lst(i+1)
            end if
        end if
    end do
    
    ! Output result
    write (*, *) sum
    
    ! Deallocate array
    deallocate(lst)
end program sum_odd_at_even_positions