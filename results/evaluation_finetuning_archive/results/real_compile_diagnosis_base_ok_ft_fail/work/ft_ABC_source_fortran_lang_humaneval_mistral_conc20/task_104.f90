program filter_odd_digits
    implicit none
    integer, parameter :: max_len = 100
    integer :: n, i, j, temp
    integer, allocatable :: x(:), result(:)
    integer :: len_result
    
    ! Read array length
    read(*, *) n
    
    ! Read array elements
    allocate(x(n))
    read(*, *) x
    
    ! Filter elements without even digits
    result = 0
    len_result = 0
    do i = 1, n
        if (has_only_odd_digits(x(i))) then
            len_result = len_result + 1
            result(len_result) = x(i)
        end if
    end do
    
    ! Sort the result
    do i = 1, len_result - 1
        do j = i + 1, len_result
            if (result(j) < result(i)) then
                temp = result(i)
                result(i) = result(j)
                result(j) = temp
            end if
        end do
    end do
    
    ! Output the result
    do i = 1, len_result
        write(*, '(I0)') result(i)
    end do
    
contains
    
    function has_only_odd_digits(num) result(has_odd)
        integer, intent(in) :: num
        logical :: has_odd
        integer :: digit
        
        has_odd = .true.
        do while (num > 0)
            digit = mod(num, 10)
            if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
                has_odd = .false.
                return
            end if
            num = num / 10
        end do
    end function has_only_odd_digits
    
end program filter_odd_digits