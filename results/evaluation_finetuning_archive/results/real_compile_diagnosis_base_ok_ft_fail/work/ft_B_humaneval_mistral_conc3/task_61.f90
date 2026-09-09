program check_brackets
  implicit none
  character(len=100) :: input
  integer :: i, count
  character(len=1) :: c
  
  read *, input
  
  count = 0
  
  do i = 1, len_trim(input)
    c = input(i:i)
    if (c == '(') then
      count = count + 1
    else if (c == ')') then
      count = count - 1
    end if
  end do
  
  if (count == 0) then
    print *, .true.
  else
    print *, .false.
  end if
  
end program check_brackets