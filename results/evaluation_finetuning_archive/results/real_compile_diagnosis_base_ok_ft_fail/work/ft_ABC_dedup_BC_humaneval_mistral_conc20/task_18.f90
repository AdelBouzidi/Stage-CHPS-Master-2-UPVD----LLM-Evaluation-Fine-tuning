program how_many_times_demo
  implicit none
  character(len=100) :: string, substring
  integer :: result

  ! Hardcoded input as per example
  string = 'aaa'
  substring = 'a'

  result = how_many_times(string, substring)
  print *, 'Result:', result

contains

  integer function how_many_times(string, substring)
    implicit none
    character(len=*), intent(in) :: string, substring
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