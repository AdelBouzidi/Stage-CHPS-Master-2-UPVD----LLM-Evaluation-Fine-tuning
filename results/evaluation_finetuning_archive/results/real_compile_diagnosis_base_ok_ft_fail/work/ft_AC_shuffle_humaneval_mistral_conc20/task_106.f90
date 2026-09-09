program factorial_sum_demo
    implicit none
    integer :: n
    integer, allocatable :: result(:)
    
    ! Read input
    read(*,*) n
    
    ! Allocate and compute result
    allocate(result(n))
    call compute_factorial_sum(n, result)
    
    ! Print output
    print *, result
    
contains

    subroutine compute_factorial_sum(n, result)
        implicit none
        integer, intent(in) :: n
        integer, intent(out) :: result(*)
        integer :: i
        integer :: factorial, sum_val
        
        do i = 1, n
            if (mod(i, 2) == 0) then
                ! Even index: compute factorial
                factorial = 1
                do while (i > 1)
                    factorial = factorial * i
                    i = i - 1
                end do
                result(i) = factorial
            else
                ! Odd index: compute sum from 1 to i
                sum_val = 0
                do while (i > 0)
                    sum_val = sum_val + i
                    i = i - 1
                end do
                result(i) = sum_val
            end if
        end do
    end subroutine compute_factorial_sum

end program factorial_sum_demo