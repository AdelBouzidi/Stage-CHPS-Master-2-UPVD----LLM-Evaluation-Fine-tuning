program how_many_times
  implicit none
  character(len=*) :: string, substring
  integer :: count

  ! Hardcoded input values
  string = 'aaa'
  substring = 'a'

  count = how_many_times(string, substring)

  print *, count

contains

  integer function how_many_times(string, substring)
    implicit none
    character(len=*), intent(in) :: string, substring
    integer :: i, j, len_str, len_sub, count

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

end program how_many_times