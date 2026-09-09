program solution_demo
    implicit none
    integer, parameter :: MAX_LEN = 100
    integer :: lst_len
    integer, dimension(MAX_LEN) :: lst
    integer :: i, sum

    ! Read input
    read(*,*) lst_len
    read(*,*) (lst(i), i=1, lst_len)

    ! Calculate sum of odd elements at even positions (1-indexed)
    sum = 0
    do i = 2, lst_len, 2
        if (mod(lst(i), 2) /= 0) then
            sum = sum + lst(i)
        end if
    end do

    ! Output result
    print *, sum

end program solution_demo