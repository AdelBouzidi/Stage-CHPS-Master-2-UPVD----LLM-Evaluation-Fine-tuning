program factorial_sum_demo
    implicit none
    integer, parameter :: dp = kind(1.0d0)
    integer :: n
    integer, allocatable :: result(:)
    integer :: i

    ! Read input from stdin
    read(*,*) n

    ! Call the function
    result = factorial_sum(n)

    ! Print the result
    print *, result

contains

    function factorial_sum(n) result(res)
        implicit none
        integer, intent(in) :: n
        integer, allocatable :: res(:)
        integer :: i
        integer :: sum_val
        integer :: fact_val

        allocate(res(n))

        do i = 1, n
            if (mod(i, 2) == 0) then
                fact_val = 1
                do
                    if (i <= fact_val) exit
                    fact_val = fact_val * i
                end do
                res(i) = fact_val
            else
                sum_val = 0
                do
                    if (i <= sum_val) exit
                    sum_val = sum_val + i
                end do
                res(i) = sum_val
            end if
        end do
    end function factorial_sum

end program factorial_sum_demo