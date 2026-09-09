program rescale_to_unit
    implicit none
    integer, parameter :: max_len = 100
    integer :: n
    real, dimension(max_len) :: numbers
    real :: min_val, max_val
    real :: rescaled
    integer :: i
    
    ! Read number of elements
    read(*,*) n
    
    ! Read the array elements
    do i = 1, n
        read(*,*) numbers(i)
    end do
    
    ! Find min and max
    min_val = numbers(1)
    max_val = numbers(1)
    do i = 2, n
        if (numbers(i) < min_val) min_val = numbers(i)
        if (numbers(i) > max_val) max_val = numbers(i)
    end do
    
    ! Apply linear transform
    if (max_val == min_val) then
        ! All values are the same, output zeros
        do i = 1, n
            write(*,*) 0.0
        end do
    else
        do i = 1, n
            rescaled = (numbers(i) - min_val) / (max_val - min_val)
            write(*,*) rescaled
        end do
    end if
    
end program rescale_to_unit