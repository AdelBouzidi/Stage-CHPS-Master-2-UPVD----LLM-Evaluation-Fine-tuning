program collatz_odds
    implicit none
    integer :: n
    integer, allocatable :: odd_collatz(:)
    integer :: i, temp, j, temp_val

    ! Read input
    read(*,*) n

    ! Generate Collatz sequence and collect odd numbers
    odd_collatz = 0
    i = 0
    temp = n
    do while (temp > 0)
        if (mod(temp, 2) == 1) then
            i = i + 1
            odd_collatz(i) = temp
        end if
        if (temp == 1) exit
        if (mod(temp, 2) == 0) then
            temp = temp / 2
        else
            temp = 3 * temp + 1
        end if
    end do

    ! Sort the odd numbers (simple bubble sort)
    do i = 1, i - 1
        do j = i + 1, i
            if (odd_collatz(j) < odd_collatz(i)) then
                temp_val = odd_collatz(i)
                odd_collatz(i) = odd_collatz(j)
                odd_collatz(j) = temp_val
            end if
        end do
    end do

    ! Output the sorted odd numbers
    do i = 1, i
        print *, odd_collatz(i)
    end do

end program collatz_odds