program main
        implicit none
        character(len=100) :: s
        character(len=100) :: result
        integer :: i

        function decode_shift(string s)
        implicit none
        character(len=100) :: s
        character(len=100) :: decode_shift
        integer :: i
        do i = 1, len(s)
            if (s(i:i) >= 'a' .and. s(i:i) <= 'z') then
                decode_shift = char(ieor(s(i:i), 5))
            else if (s(i:i) >= 'A' .and. s(i:i) <= 'Z') then
                decode_shift = char(ieor(s(i:i), 5))
            else
                decode_shift = s(i:i)
            end if
        end do
        end function decode_shift

        read *, s
        result = decode_shift(s)
        write (*, '(A)') result
        end program main