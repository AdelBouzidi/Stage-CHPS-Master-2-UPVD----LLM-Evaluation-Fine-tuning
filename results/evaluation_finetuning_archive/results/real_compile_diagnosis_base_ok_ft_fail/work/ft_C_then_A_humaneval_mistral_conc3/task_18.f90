program how_many_times
  implicit none
  character(len=*), parameter :: string = 'aaa'
  character(len=*), parameter :: substring = 'a'
  integer :: count
  count = how_many_times(string, substring)
  print *, count
contains
  integer function how_many_times(string, substring)
    character(len=*), intent(in) :: string
    character(len=*), intent(in) :: substring
    integer :: i, len_str, len_sub
    len_str = len_trim(string)
    len_sub = len_trim(substring)
    if (len_sub > len_str) then
      how_many_times = 0
      return
    end if
    how_many_times = 0
    do i = 1, len_str - len_sub + 1
      if (string(i:i+len_sub-1) == substring) then
        how_many_times = how_many_times + 1
      end if
    end do
  end function how_many_times
end program how_many_times