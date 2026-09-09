program decode_shift_demo
  implicit none
  character(len=100) :: s
  character(len=100) :: result

  ! Read input string
  read(*, '(A)') s

  ! Call decode_shift function
  call decode_shift(s, result)

  ! Output result
  print *, result

contains

  subroutine decode_shift(s, result)
    implicit none
    character(len=*), intent(in) :: s
    character(len=*), intent(out) :: result
    integer :: i, len
    character(len=1) :: c

    len = len_trim(s)
    result = ''
    do i = 1, len
      c = s(i:i)
      if (c >= 'a' .and. c <= 'z') then
        c = char(ichar(c) - 5)
      else if (c >= 'A' .and. c <= 'Z') then
        c = char(ichar(c) - 5)
      end if
      result = result // c
    end do
  end subroutine decode_shift

end program decode_shift_demo