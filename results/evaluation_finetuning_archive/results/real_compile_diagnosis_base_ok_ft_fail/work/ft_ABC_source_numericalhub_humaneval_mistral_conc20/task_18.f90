program test_how_many_times
  implicit none
  integer, parameter :: i4b = selected_int_kind(9)
  character(len=100) :: string, substring
  integer :: result

  ! Read input from stdin
  read(*,*) string, substring
  result = how_many_times(string, substring)
  print *, result

contains

  integer function how_many_times(string, substring)
    character(len=*), intent(in) :: string, substring
    integer :: i, n, m, count
    character(len=len(string)) :: temp

    n = len(string)
    m = len(substring)
    count = 0
    do i = 1, n - m + 1
      if (string(i:i+m-1) == substring) then
        count = count + 1
      end if
    end do
    how_many_times = count
  end function how_many_times

end program test_how_many_times