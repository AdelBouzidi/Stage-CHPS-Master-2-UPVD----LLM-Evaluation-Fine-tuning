program prime_factors
    implicit none
    integer :: n, i
    integer, allocatable :: factors(:)
    integer :: factor_count
    
    ! Read input
    read *, n
    
    ! Initialize factors array
    factor_count = 0
    
    ! Find prime factors
    i = 2
    do while (i * i <= n)
        do while (mod(n, i) == 0)
            factor_count = factor_count + 1
            factors(factor_count) = i
            n = n / i
        end do
        i = i + 1
    end do
    
    ! If n > 1, then the remaining n is a prime factor
    if (n > 1) then
        factor_count = factor_count + 1
        factors(factor_count) = n
    end if
    
    ! Output the factors
    if (factor_count > 0) then
        do i = 1, factor_count
            write (*, '(I0)') factors(i)
            if (i < factor_count) write (*, '(A)') ' '
        end do
    end if
    
end program prime_factors