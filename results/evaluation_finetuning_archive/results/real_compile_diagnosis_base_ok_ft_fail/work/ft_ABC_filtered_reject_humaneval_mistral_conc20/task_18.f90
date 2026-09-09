program main
  implicit none
  character(len=100) :: string, substring
  integer :: result

  ! Read input
  read(*, '(A)') string
  read(*, '(A)') substring

  ! Call the function
  result = how_many_times(string, substring)

  ! Print output
  print *, result

contains

  function how_many_times(string, substring) result(res)
    implicit none
    character(len=*), intent(in) :: string, substring
    integer :: res
    integer :: i, len_str, len_sub

    res = 0
    len_str = len(string)
    len_sub = len(substring)

    if (len_sub > len_str) then
      return
    end if

    do i = 1, len_str - len_sub + 1
      if (string(i:i+len_sub-1) == substring) then
        res = res + 1
      end if
    end do

  end function how_many_times

end program main