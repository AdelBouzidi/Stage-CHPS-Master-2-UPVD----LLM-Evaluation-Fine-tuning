program decode_shift_demo
  implicit none
  character(len=3) :: input_str
  character(len=3) :: output_str
  
  read(*, '(a)') input_str
  output_str = decode_shift(input_str)
  print *, output_str
  
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