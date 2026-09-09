program collatz_odds
    implicit none
    integer :: n
    integer, allocatable :: odd_collatz(:)
    integer :: i, temp
    integer :: count
    
    read *, n
    
    temp = n
    count = 0
    do while (temp >= 1)
        if (mod(temp, 2) == 1) then
            count = count + 1
        end if
        if (temp == 1) exit
        if (mod(temp, 2) == 0) then
            temp = temp / 2
        else
            temp = 3 * temp + 1
        end if
    end do
    
    allocate(odd_collatz(count))
    
    temp = n
    i = 1
    do while (temp >= 1)
        if (mod(temp, 2) == 1) then
            odd_collatz(i) = temp
            i = i + 1
        end if
        if (temp == 1) exit
        if (mod(temp, 2) == 0) then
            temp = temp / 2
        else
            temp = 3 * temp + 1
        end if
    end do
    
    do i = 1, count
        write (*, '(I0)') odd_collatz(i)
        if (i < count) write (*, '(A)') ' '
    end do
    
end program collatz_odds