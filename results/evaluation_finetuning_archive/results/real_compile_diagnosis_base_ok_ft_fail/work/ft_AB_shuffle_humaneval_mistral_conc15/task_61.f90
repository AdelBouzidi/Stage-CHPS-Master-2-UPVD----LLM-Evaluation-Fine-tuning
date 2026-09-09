program correct_bracketing
  implicit none
  character(len=*), parameter :: input = '(('
  logical :: result

  result = correct_bracketing(input)
  print *, result

contains

  logical function correct_bracketing(brackets)
    implicit none
    character(len=*), intent(in) :: brackets
    integer :: open_count, i, len
    character(len=1) :: ch

    open_count = 0
    len = len_trim(brackets)
    
    do i = 1, len
      ch = brackets(i:i)
      if (ch == '(') then
        open_count = open_count + 1
      else if (ch == ')') then
        open_count = open_count - 1
      end if
    end do
    
    correct_bracketing = (open_count == 0)
  end function correct_bracketing

end program correct_bracketing