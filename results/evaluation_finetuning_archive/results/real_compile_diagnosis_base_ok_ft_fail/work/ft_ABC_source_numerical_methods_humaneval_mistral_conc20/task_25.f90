program prime_factors
    implicit none
    integer :: n, i
    integer, dimension(100) :: factors
    integer :: count
    
    ! Read input
    read(*,*) n
    
    ! Handle edge cases
    if (n <= 1) then
        write(*,*)
        stop
    end if
    
    ! Find prime factors
    count = 0
    i = 2
    do while (i * i <= n)
        do while (mod(n, i) == 0)
            count = count + 1
            factors(count) = i
            n = n / i
        end do
        i = i + 1
    end do
    
    ! If n > 1, then the remaining n is prime
    if (n > 1) then
        count = count + 1
        factors(count) = n
    end if
    
    ! Output the factors
    do i = 1, count
        if (i > 1) write(*,*) ' '
        write(*,*) factors(i)
    end do
    
end program prime_factors