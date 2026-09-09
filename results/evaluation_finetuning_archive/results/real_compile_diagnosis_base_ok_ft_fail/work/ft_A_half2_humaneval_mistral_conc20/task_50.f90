program decode_shift_demo
  implicit none
  character(len=*) :: input
  character(len=*) :: result

  ! Read input from stdin
  read(*, '(a)') input

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

    res = ''
    do i = 1, len_trim(s)
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        c = char(ichar(c) - 5)
      else if (c >= 'A' .and. c <= 'Z') then
        c = char(ichar(c) - 5)
      end if
      res = trim(res) // c
    end do
  end function decode_shift

end program decode_shift_demo