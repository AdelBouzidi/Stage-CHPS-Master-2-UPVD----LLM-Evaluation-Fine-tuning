program how_many_times_demo
  implicit none
  character(len=100) :: string
  character(len=100) :: substring
  integer :: result

  read *, string
  read *, substring
  result = how_many_times(string, substring)
  print *, result

contains

  integer function how_many_times(string, substring)
    character(len=*), intent(in) :: string
    character(len=*), intent(in) :: substring
    integer :: i, count
    integer :: len_str, len_sub
    len_str = len_trim(string)
    len_sub = len_trim(substring)
    count = 0
    if (len_sub <= len_str) then
      do i = 1, len_str - len_sub + 1
        if (string(i:i+len_sub-1) == substring) then
          count = count + 1
        end if
      end do
    end if
    how_many_times = count
  end function how_many_times

end program how_many_times_demo