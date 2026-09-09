program how_many_times
  implicit none
  character(len=*), parameter :: string = 'aaa'
  character(len=*), parameter :: substring = 'a'
  integer :: count
  count = how_many_times(string, substring)
  print *, count
contains
  integer function how_many_times(str, sub)
    character(len=*), intent(in) :: str
    character(len=*), intent(in) :: sub
    integer :: i, len_str, len_sub
    len_str = len_trim(str)
    len_sub = len_trim(sub)
    if (len_sub > len_str) then
      how_many_times = 0
      return
    end if
    how_many_times = 0
    do i = 1, len_str - len_sub + 1
      if (str(i:i+len_sub-1) == sub) then
        how_many_times = how_many_times + 1
      end if
    end do
  end function how_many_times
end program how_many_times