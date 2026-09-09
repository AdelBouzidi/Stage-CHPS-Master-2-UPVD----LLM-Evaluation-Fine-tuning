program how_many_times_demo
  implicit none
  character(len=*), dimension(2) :: input
  integer :: result

  ! Read input strings
  read(*, '(2A)') input

  ! Call the function
  result = how_many_times(input(1), input(2))

  ! Output result
  print *, result

contains

  integer function how_many_times(string, substring)
    implicit none
    character(len=*), intent(in) :: string, substring
    integer :: i, count, len_str, len_sub

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