program main
        implicit none
        integer, parameter :: x_len = 4
        integer, dimension(x_len) :: x = [15, 33, 1422, 1]
        integer, dimension(:), allocatable :: y
        y = unique_digits(x_len, x)
        print *, y
        end program main