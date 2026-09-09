program decode_shift_demo
  implicit none
  character(len=:), allocatable :: input_str, output_str
  integer :: i

  ! Read input from stdin
  read *, input_str

  ! Call the decode_shift function
  output_str = decode_shift(input_str)

  ! Print the result
  print *, 'Decoded string:', trim(output_str)

contains

  function decode_shift(s) result(decoded)
    implicit none
    character(len=*), intent(in) :: s
    character(len=len(s)) :: decoded
    integer :: i
    character(len=1) :: c, shifted

    do i = 1, len(s)
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        shifted = char(ichar(c) - 5)
      else if (c >= 'A' .and. c <= 'Z') then
        shifted = char(ichar(c) - 5)
      else
        shifted = c
      end if
      decoded(i:i) = shifted
    end do
  end function decode_shift

end program decode_shift_demo