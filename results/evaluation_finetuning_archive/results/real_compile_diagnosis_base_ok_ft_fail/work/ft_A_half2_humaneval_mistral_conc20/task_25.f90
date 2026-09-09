program factorize_demo
    implicit none
    integer :: n
    integer, allocatable :: factors(:)
    
    ! Read input
    read(*,*) n
    
    ! Call the factorize function
    call factorize(n, factors)
    
    ! Print output
    print *, factors
    deallocate(factors)
    
contains

    subroutine factorize(n, factors)
        implicit none
        integer, intent(in) :: n
        integer, allocatable, intent(out) :: factors(:)
        integer :: i, count
        integer :: temp
        
        temp = n
        count = 0
        do i = 2, n
            if (mod(temp, i) == 0) then
                count = count + 1
            else
                exit
            end if
        end do
        allocate(factors(count))
        i = 1
        do while (i <= count)
            factors(i) = 2
            i = i + 1
        end do
    end subroutine factorize

end program factorize_demo