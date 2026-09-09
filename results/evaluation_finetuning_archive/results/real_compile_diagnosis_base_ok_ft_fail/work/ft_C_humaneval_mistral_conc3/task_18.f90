program count_substring
    implicit none
    character(len=*), intent(in) :: string, substring
    integer :: count, i, len_str, len_sub
    
    ! Get input from stdin
    read(*, '(A)') string
    read(*, '(A)') substring
    
    ! Calculate lengths
    len_str = len_trim(string)
    len_sub = len_trim(substring)
    
    ! Count overlapping occurrences
    count = 0
    if (len_sub <= len_str) then
        do i = 1, len_str - len_sub + 1
            if (string(i:i+len_sub-1) == substring) then
                count = count + 1
            end if
        end do
    end if
    
    ! Output the count
    print *, count
end program count_substring