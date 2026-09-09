program how_many_times_demo
  implicit none
  character(len=100) :: string
  character(len=100) :: substring
  integer :: result

  ! Read input
  read(*, '(a)') string
  read(*, '(a)') substring

  ! Call the function
  result = how_many_times(string, substring)

  ! Output result
  print *, result

contains

  function how_many_times(string, substring) result(res)
    implicit none
    character(len=*), intent(in) :: string
    character(len=*), intent(in) :: substring
    integer :: res
    integer :: i, len_str, len_sub
    character(len=len(string)) :: str
    character(len=len(substring)) :: sub

    len_str = len_trim(string)
    len_sub = len_trim(substring)
    
    if (len_sub > len_str) then
      res = 0
    else
      res = 0
      do i = 1, len_str - len_sub + 1
        if (string(i:i+len_sub-1) == substring(1:len_sub)) then
          res = res + 1
        end if
      end do
    end if
  end function how_many_times

end program how_many_times_demo