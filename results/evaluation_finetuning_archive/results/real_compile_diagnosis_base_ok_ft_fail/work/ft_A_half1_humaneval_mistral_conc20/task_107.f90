program even_odd_palindrome_demo
    implicit none
    integer :: n
    integer :: even_count, odd_count
    integer :: i
    character(len=10) :: num_str
    character(len=10) :: reversed_str

    ! Read input
    read(*,*) n

    ! Initialize counters
    even_count = 0
    odd_count = 0

    ! Count palindromes
    do i = 1, n
        ! Convert number to string
        write(num_str, '(I0)') i
        ! Reverse the string
        call reverse_string(num_str, reversed_str)
        ! Check if palindrome
        if (num_str == reversed_str) then
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

    subroutine reverse_string(str, result)
        character(len=*), intent(in) :: str
        character(len=*), intent(out) :: result
        integer :: len, i
        len = len_trim(str)
        do i = 1, len
            result(i) = str(len - i + 1)
        end do
    end subroutine reverse_string

end program even_odd_palindrome_demo