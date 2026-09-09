program correct_bracketing
  implicit none
  character(len=100) :: brackets
  logical :: result
  read *, brackets
  result = correct_bracketing(brackets)
  print *, result
contains
  function correct_bracketing(brackets) result(res)
    implicit none
    character(len=*), intent(in) :: brackets
    logical :: res
    integer :: i, open_count
    open_count = 0
    do i = 1, len(brackets)
      if (brackets(i:i) == '(') then
        open_count = open_count + 1
      else if (brackets(i:i) == ')') then
        open_count = open_count - 1
      end if
    end do
    res = (open_count == 0)
  end function correct_bracketing
end program correct_bracketing