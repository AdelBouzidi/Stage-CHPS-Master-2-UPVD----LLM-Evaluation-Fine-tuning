program correct_bracketing
  implicit none
  character(len=100) :: brackets
  integer :: i, n
  logical :: result

  ! Read input from stdin
  read(*, '(A)') brackets

  ! Initialize result
  result = .true.

  ! Count opening and closing brackets
  n = 0
  do i = 1, len(brackets)
    if (brackets(i:i) == '(') then
      n = n + 1
    else if (brackets(i:i) == ')') then
      n = n - 1
    end if
  end do

  ! Check if brackets are correctly matched
  if (n /= 0) then
    result = .false.
  end if

  ! Output result
  print *, result

end program correct_bracketing