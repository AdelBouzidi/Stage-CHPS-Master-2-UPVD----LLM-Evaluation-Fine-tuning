program correct_bracketing
  implicit none
  character(len=100) :: input_str
  logical :: result
  integer :: i, count

  ! Read input from stdin
  read *, input_str

  ! Initialize count for tracking brackets
  count = 0

  ! Check each character in the string
  do i = 1, len_trim(input_str)
    select case (input_str(i:i))
    case ('(')
      count = count + 1
    case (')')
      count = count - 1
    case default
      ! Ignore other characters
    end select
  end do

  ! Check if all brackets are matched
  result = (count == 0)

  ! Output the result
  print *, result

end program correct_bracketing