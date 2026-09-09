program correct_bracketing
  implicit none
  character(len=100) :: input_str
  integer :: i, count_open, count_close
  logical :: result

  read *, input_str

  count_open = 0
  count_close = 0

  do i = 1, len_trim(input_str)
    if (input_str(i:i) == '(') then
      count_open = count_open + 1
    else if (input_str(i:i) == ')') then
      count_close = count_close + 1
    end if
  end do

  result = (count_open == count_close)

  print *, result

end program correct_bracketing