program is_equal_to_sum_even
    implicit none
    integer :: n
    logical :: result

    ! Read input from stdin
    read(*,*) n

    ! Check if n can be written as sum of 4 positive even numbers
    result = (n > 8) .and. (mod(n, 2) == 0)

    ! Output the result
    print *, result
end program is_equal_to_sum_even