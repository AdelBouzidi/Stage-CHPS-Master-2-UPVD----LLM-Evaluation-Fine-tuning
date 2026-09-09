program bracket_check
  implicit none
  character(len=100) :: brackets
  logical :: result

  ! Hardcoded input
  brackets = "( )"

  result = correct_bracketing(brackets)

  print *, result

contains

  logical function correct_bracketing(brackets)
    implicit none
    character(len=*), intent(in) :: brackets
    integer :: i, open_count

    open_count = 0
    do i = 1, len(brackets)
      if (brackets(i:i) == '(') then
        open_count = open_count + 1
      else if (brackets(i:i) == ')') then
        open_count = open_count - 1
        if (open_count < 0) then
          correct_bracketing = .false.
          return
        end if
      end if
    end do

    correct_bracketing = (open_count == 0)
  end function correct_bracketing

end program bracket_check