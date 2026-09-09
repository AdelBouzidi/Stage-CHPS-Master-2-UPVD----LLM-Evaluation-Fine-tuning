program decode_shift_demo
  implicit none
  character(len=*), parameter :: input = 'fgh'
  character(len=:), allocatable :: result

  call decode_shift(input, result)
  print *, result

contains

  subroutine decode_shift(s, out)
    implicit none
    character(len=*), intent(in) :: s
    character(len=:), allocatable, intent(out) :: out
    integer :: i, n, c
    character(len=1) :: ch

    n = len_trim(s)
    allocate(character(len=n) :: out)

    do i = 1, n
      ch = s(i:i)
      c = iachar(ch)
      if (c >= iachar('a') .and. c <= iachar('z')) then
        c = c - 5
        if (c < iachar('a')) c = c + 26
      else if (c >= iachar('A') .and. c <= iachar('Z')) then
        c = c - 5
        if (c < iachar('A')) c = c + 26
      end if
      out(i:i) = achar(c)
    end do

  end subroutine decode_shift

end program decode_shift_demo