program decode_shift_demo
  implicit none
  character(len=:), allocatable :: input, result
  integer :: i, len

  ! Read input from stdin
  read *, input

  ! Get the length of the input string
  len = len_trim(input)
  allocate(character(len=len) :: result)

  ! Decode the string by shifting each character back by 5
  do i = 1, len
    if (input(i:i) >= 'a' .and. input(i:i) <= 'z') then
      result(i:i) = char(ichar(input(i:i)) - 5)
    else if (input(i:i) >= 'A' .and. input(i:i) <= 'Z') then
      result(i:i) = char(ichar(input(i:i)) - 5)
    else
      result(i:i) = input(i:i)
    end if
  end do

  print *, result

end program decode_shift_demo