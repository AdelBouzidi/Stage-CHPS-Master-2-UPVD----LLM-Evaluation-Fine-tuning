program even_odd_palindrome
    implicit none
    integer :: n
    integer :: even_count, odd_count
    integer :: i
    logical :: is_palindrome

    ! Read input
    read(*,*) n

    ! Initialize counters
    even_count = 0
    odd_count = 0

    ! Check each number from 1 to n
    do i = 1, n
        if (is_palindrome(i)) then
            if (mod(i, 2) == 0) then
                even_count = even_count + 1
            else
                odd_count = odd_count + 1
            end if
        end if
    end do

    ! Output results
    print *, even_count, odd_count

contains

    logical function is_palindrome(num)
        integer, intent(in) :: num
        integer :: temp
        integer :: reversed
        integer :: digit
        reversed = 0
        temp = num
        do while (temp > 0)
            digit = mod(temp, 10)
            reversed = reversed * 10 + digit
            temp = temp / 10
        end do
        is_palindrome = (reversed == num)
    end function is_palindrome

end program even_odd_palindrome