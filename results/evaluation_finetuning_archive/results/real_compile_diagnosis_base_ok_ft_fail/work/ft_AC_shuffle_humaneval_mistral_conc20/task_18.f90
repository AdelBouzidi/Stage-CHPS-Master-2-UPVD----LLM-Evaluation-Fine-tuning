program main
  implicit none
  character(len=100) :: string, substring
  integer :: count

  ! Hardcoded input values
  string = 'aaa'
  substring = 'a'

  ! Call the function
  count = how_many_times(string, substring)

  ! Output the result
  print *, 'Count:', count

contains

  function how_many_times(string, substring) result(count)
    implicit none
    character(len=*), intent(in) :: string, substring
    integer :: count
    integer :: i, len_str, len_sub

    len_str = len_trim(string)
    len_sub = len_trim(substring)

    if (len_sub > len_str) then
      count = 0
      return
    end if

    count = 0
    do i = 1, len_str - len_sub + 1
      if (string(i:i+len_sub-1) == substring) then
        count = count + 1
      end if
    end do
  end function how_many_times

end program main