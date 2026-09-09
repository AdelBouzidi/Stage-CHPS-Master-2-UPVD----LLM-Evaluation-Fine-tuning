program filter_odd_digits
    implicit none
    integer, allocatable :: x(:)
    integer :: n, i, j, temp
    integer :: filtered_count
    integer, allocatable :: filtered(:)
    integer :: digit

    ! Read array length
    read(*, *) n

    ! Read array elements
    allocate(x(n))
    read(*, *) x

    ! Filter elements that don't contain any even digit
    filtered_count = 0
    allocate(filtered(n))
    do i = 1, n
        if (has_only_odd_digits(x(i))) then
            filtered_count = filtered_count + 1
            filtered(filtered_count) = x(i)
        end if
    end do

    ! Sort the filtered array
    do i = 1, filtered_count - 1
        do j = i + 1, filtered_count
            if (filtered(i) > filtered(j)) then
                temp = filtered(i)
                filtered(i) = filtered(j)
                filtered(j) = temp
            end if
        end do
    end do

    ! Output the result
    do i = 1, filtered_count
        write(*, *) filtered(i)
    end do

contains

    function has_only_odd_digits(num) result(result)
        integer, intent(in) :: num
        logical :: result
        integer :: digit

        result = .true.
        do while (num > 0)
            digit = mod(num, 10)
            if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
                result = .false.
                return
            end if
            num = num / 10
        end do
    end function has_only_odd_digits

end program filter_odd_digits