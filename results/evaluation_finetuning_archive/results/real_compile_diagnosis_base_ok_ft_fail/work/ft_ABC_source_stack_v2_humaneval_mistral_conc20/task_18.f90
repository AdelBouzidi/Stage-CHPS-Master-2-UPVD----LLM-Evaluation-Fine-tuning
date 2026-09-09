program how_many_times_demo
  implicit none
  character(len=*), parameter :: string = "aaa"
  character(len=*), parameter :: substring = "a"
  integer :: result

  result = how_many_times(string, substring)
  print *, result

contains

  integer function how_many_times(string, substring)
    character(len=*), intent(in) :: string
    character(len=*), intent(in) :: substring
    integer :: i, j, len_str, len_sub
    logical :: match

    len_str = len_trim(string)
    len_sub = len_trim(substring)

    if (len_sub > len_str) then
      how_many_times = 0
      return
    end if

    how_many_times = 0
    do i = 1, len_str - len_sub + 1
      match = .true.
      do j = 1, len_sub
        if (string(i+j-1:i+j-1) /= substring(j:j)) then
          match = .false.
          exit
        end if
      end do
      if (match) then
        how_many_times = how_many_times + 1
      end if
    end do
  end function how_many_times

end program how_many_times_demo