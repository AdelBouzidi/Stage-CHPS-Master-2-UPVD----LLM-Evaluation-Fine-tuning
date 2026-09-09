program how_many_times_demo
  implicit none
  character(len=*) :: str, sub
  integer :: result
  
  read *, str
  read *, sub
  result = how_many_times(str, sub)
  print *, result
contains

  integer function how_many_times(string, substring)
    character(len=*), intent(in) :: string
    character(len=*), intent(in) :: substring
    integer :: i, count
    integer :: len_str, len_sub
    
    len_str = len_trim(string)
    len_sub = len_trim(substring)
    
    if (len_sub > len_str) then
      how_many_times = 0
      return
    end if
    
    count = 0
    do i = 1, len_str - len_sub + 1
      if (string(i:i+len_sub-1) == substring) then
        count = count + 1
      end if
    end do
    
    how_many_times = count
  end function how_many_times

end program how_many_times_demo