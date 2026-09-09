program decode_shift_demo
  implicit none
  character(len=*) :: input_str
  character(len=*) :: result

  ! Read input from stdin
  read *, input_str

  ! Call decode_shift function
  result = decode_shift(input_str)

  ! Print result
  print *, result

contains

  function decode_shift(s) result(res)
    implicit none
    character(len=*), intent(in) :: s
    character(len=len(s)) :: res
    integer :: i, n
    character(len=1) :: c

    n = len(s)
    res = s
    do i = 1, n
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