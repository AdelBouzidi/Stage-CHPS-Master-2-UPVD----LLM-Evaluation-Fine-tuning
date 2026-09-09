program correct_bracketing_test
  implicit none
  character(len=100) :: input_str
  logical :: result
  integer :: i, count_open, count_close

  ! Read input from stdin
  read *, input_str

  ! Initialize counters
  count_open = 0
  count_close = 0

  ! Count brackets in the input string
  do i = 1, len_trim(input_str)
    if (input_str(i:i) == '(') then
      count_open = count_open + 1
    else if (input_str(i:i) == ')') then
      count_close = count_close + 1
    end if
  end do

  ! Check if bracketing is correct
  result = (count_open == count_close)

  print *, result

end program correct_bracketing_test