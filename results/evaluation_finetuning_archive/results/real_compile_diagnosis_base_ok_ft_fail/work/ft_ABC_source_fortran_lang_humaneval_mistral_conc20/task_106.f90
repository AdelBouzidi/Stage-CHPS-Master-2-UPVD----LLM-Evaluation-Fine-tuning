program factorial_sum_array
    implicit none
    integer :: n, i, j
    integer, allocatable :: result(:)
    
    ! Read input
    read *, n
    
    ! Allocate array
    allocate(result(n))
    
    ! Compute values
    do i = 1, n
        if (mod(i, 2) == 0) then
            ! Even: factorial
            result(i) = 1
            do j = 1, i
                result(i) = result(i) * j
            end do
        else
            ! Odd: sum from 1 to i
            result(i) = i * (i + 1) / 2
        end if
    end do
    
    ! Output
    do i = 1, n
        write (*, '(I0)') result(i)
        if (i < n) write (*, '(A)') ' '
    end do
    
    ! Clean up
    deallocate(result)
    
end program factorial_sum_array