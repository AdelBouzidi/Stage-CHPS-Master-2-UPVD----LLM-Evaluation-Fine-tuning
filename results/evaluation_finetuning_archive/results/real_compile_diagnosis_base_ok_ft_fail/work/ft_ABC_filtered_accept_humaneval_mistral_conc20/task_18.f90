program how_many_times_demo
  implicit none
  character(len=*) :: string, substring
  integer :: count
  read *, string
  read *, substring
  count = how_many_times(string, substring)
  print *, count
contains
  function how_many_times(string, substring) result(count)
    implicit none
    character(len=*), intent(in) :: string, substring
    integer :: count
    integer :: i, len_str, len_sub
    len_str = len_trim(string)
    len_sub = len_trim(substring)
    count = 0
    if (len_sub > len_str) then
      count = 0
    else
      do i = 1, len_str - len_sub + 1
        if (string(i:i+len_sub-1) == substring) then
          count = count + 1
        end if
      end do
    end if
  end function how_many_times
end program how_many_times_demo