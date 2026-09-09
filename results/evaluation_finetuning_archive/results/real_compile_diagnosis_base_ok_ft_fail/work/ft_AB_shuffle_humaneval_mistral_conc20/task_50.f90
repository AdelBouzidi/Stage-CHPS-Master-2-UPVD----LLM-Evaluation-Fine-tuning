program decode_shift_demo
  implicit none
  character(len=*), parameter :: input = 'fgh'
  character(len=len(input)) :: output
  integer :: i

  output = decode_shift(input)
  print *, output

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
        if (c >= 'f') then
          res(i:i) = char(ichar(c) - 5)
        else
          res(i:i) = char(ichar(c) - 5 + 26)
        end if
      else if (c >= 'A' .and. c <= 'Z') then
        if (c >= 'F') then
          res(i:i) = char(ichar(c) - 5)
        else
          res(i:i) = char(ichar(c) - 5 + 26)
        end if
      else
        res(i:i) = c
      end if
    end do

    res = res
  end function decode_shift

end program decode_shift_demo