program vowel_counter
    implicit none
    character(len=*) :: s
    integer :: count, i, len_s
    character :: c
    
    read *, s
    count = 0
    len_s = len_trim(s)
    
    do i = 1, len_s
        c = trim(s(i:i))
        select case (c)
        case ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
            count = count + 1
        case ('y', 'Y')
            if (i == len_s) then
                count = count + 1
            end if
        end select
    end do
    
    print *, count
end program vowel_counter