program main
  implicit none
  character(len=100) :: s
  character(len=100) :: result
  integer :: i

  ! Read input
  read *, s

  ! Call decode_shift function
  result = decode_shift(s)

  ! Print output
  print *, result

contains

  function decode_shift(s)
    implicit none
    character(len=*), intent(in) :: s
    character(len=len(s)) :: decode_shift
    integer :: i
    character :: c

    do i = 1, len(s)
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        decode_shift(i:i) = char(ichar(c) - 5)
      else if (c >= 'A' .and. c <= 'Z') then
        decode_shift(i:i) = char(ichar(c) - 5)
      else
        decode_shift(i:i) = c
      end if
    end do

  end function decode_shift

end program main