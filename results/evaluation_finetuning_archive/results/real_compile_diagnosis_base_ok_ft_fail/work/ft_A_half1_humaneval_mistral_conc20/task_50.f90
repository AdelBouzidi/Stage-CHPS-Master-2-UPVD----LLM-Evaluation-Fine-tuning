program decode_shift_demo
  implicit none
  character(len=*) :: input
  character(len=*) :: result

  read *, input
  call decode_shift(input, result)
  print *, result

contains

  subroutine decode_shift(s, result)
    character(len=*), intent(in) :: s
    character(len=*), intent(out) :: result
    integer :: i, len_s

    len_s = len(s)
    do i = 1, len_s
      result(i:i) = char(ichar(s(i:i)) - 5)
    end do
  end subroutine decode_shift

end program decode_shift_demo