program vowel_counter
    implicit none
    character(len=*) :: input
    integer :: count
    integer :: i
    character(len=1) :: ch
    logical :: is_vowel
    integer :: len_str

    read *, input
    len_str = len_trim(input)
    count = 0

    do i = 1, len_str
        ch = input(i:i)
        is_vowel = .false.
        if (ch == 'a' .or. ch == 'e' .or. ch == 'i' .or. ch == 'o' .or. ch == 'u' .or. &
            ch == 'A' .or. ch == 'E' .or. ch == 'I' .or. ch == 'O' .or. ch == 'U') then
            is_vowel = .true.
        else if (ch == 'y' .or. ch == 'Y') then
            if (i == len_str) then
                is_vowel = .true.
            end if
        end if

        if (is_vowel) then
            count = count + 1
        end if
    end do

    print *, count

end program vowel_counter