program decode_shift
    implicit none
    character(len=100) :: encoded
    character(len=100) :: decoded
    integer :: i
    integer :: char_code
    integer :: shift_back = 5
    integer :: alphabet_size = 26

    read *, encoded
    
    do i = 1, len_trim(encoded)
        char_code = iachar(encoded(i:i))
        
        if (char_code >= ichar('a') .and. char_code <= ichar('z')) then
            char_code = char_code - shift_back
            if (char_code < ichar('a')) then
                char_code = char_code + alphabet_size
            end if
            decoded(i:i) = achar(char_code)
        else if (char_code >= ichar('A') .and. char_code <= ichar('Z')) then
            char_code = char_code - shift_back
            if (char_code < ichar('A')) then
                char_code = char_code + alphabet_size
            end if
            decoded(i:i) = achar(char_code)
        else
            decoded(i:i) = encoded(i:i)
        end if
    end do
    
    print *, trim(decoded)
end program decode_shift