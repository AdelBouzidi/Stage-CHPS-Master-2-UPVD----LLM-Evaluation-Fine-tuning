program decode_shift_demo
  implicit none
  character(len=*) :: input
  character(len=len(input)) :: result
  integer :: i
  character(len=1) :: c

  ! Read input from stdin
  read *, input

  ! Call the decode_shift function
  result = decode_shift(input)
  
  ! Print the result
  print *, result
contains

  function decode_shift(s) result(res)
    implicit none
    character(len=*), intent(in) :: s
    character(len=len(s)) :: res
    integer :: i
    character(len=1) :: c
    
    do i = 1, len(s)
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        res(i:i) = char(ichar(c) - 5)
      else if (c >= 'A' .and. c <= 'Z') then
        res(i:i) = char(ichar(c) - 5)
      else
        res(i:i) = c
      end if
    end do
  end function decode_shift

end program decode_shift_demo