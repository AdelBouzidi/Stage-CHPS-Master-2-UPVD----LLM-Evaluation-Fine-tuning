program find_closest
    implicit none
    integer :: n, i, j
    real :: numbers(1000), min_diff, diff
    integer :: idx1, idx2

    ! Read array length
    read(*,*) n

    ! Read array elements
    do i = 1, n
        read(*,*) numbers(i)
    end do

    ! Initialize with first pair
    min_diff = abs(numbers(2) - numbers(1))
    idx1 = 1
    idx2 = 2

    ! Find minimum difference
    do i = 1, n-1
        do j = i+1, n
            diff = abs(numbers(j) - numbers(i))
            if (diff < min_diff) then
                min_diff = diff
                idx1 = i
                idx2 = j
            end if
        end do
    end do

    ! Output the two closest numbers in order
    if (numbers(idx1) < numbers(idx2)) then
        print*, numbers(idx1), numbers(idx2)
    else
        print*, numbers(idx2), numbers(idx1)
    end if

end program find_closest