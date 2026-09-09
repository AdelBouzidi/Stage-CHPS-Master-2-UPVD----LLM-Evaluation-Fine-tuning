program count_substring
  implicit none
  character(len=100) :: string, substring
  integer :: count, i, len_str, len_sub
  
  ! Read input
  read *, string
  read *, substring
  
  ! Get lengths
  len_str = len_trim(string)
  len_sub = len_trim(substring)
  
  ! Count occurrences (including overlapping)
  count = 0
  if (len_sub <= len_str) then
    do i = 1, len_str - len_sub + 1
      if (string(i:i+len_sub-1) == substring) then
        count = count + 1
      end if
    end do
  end if
  
  ! Output result
  print *, count
end program count_substring