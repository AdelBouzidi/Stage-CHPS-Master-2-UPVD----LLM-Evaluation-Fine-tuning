program collatz_odds
    implicit none
    integer :: n
    integer, allocatable :: odd_collatz(:)
    integer :: i, j, temp
    integer :: count
    
    ! Read input
    read *, n
    
    ! Generate Collatz sequence and collect odd numbers
    odd_collatz = 0
    count = 0
    
    do
        if (mod(n, 2) == 1) then
            count = count + 1
            odd_collatz(count) = n
        end if
        if (n == 1) exit
        if (mod(n, 2) == 0) then
            n = n / 2
        else
            n = 3 * n + 1
        end if
    end do
    
    ! Sort the odd numbers
    do i = 1, count - 1
        do j = i + 1, count
            if (odd_collatz(i) > odd_collatz(j)) then
                temp = odd_collatz(i)
                odd_collatz(i) = odd_collatz(j)
                odd_collatz(j) = temp
            end if
        end do
    end do
    
    ! Output the sorted odd numbers
    do i = 1, count
        write (*, '(I0)') odd_collatz(i)
    end do
    
end program collatz_odds