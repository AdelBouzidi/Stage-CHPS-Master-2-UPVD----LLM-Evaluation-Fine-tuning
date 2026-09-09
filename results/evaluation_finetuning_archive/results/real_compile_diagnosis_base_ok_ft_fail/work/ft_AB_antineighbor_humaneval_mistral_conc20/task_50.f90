program decode_shift_demo
  implicit none
  character(len=*), parameter :: input = "fgh"
  character(len=:), allocatable :: result
  integer :: i, n
  character(len=1) :: c

  ! Decode the input string
  result = ""
  n = len_trim(input)
  do i = 1, n
    c = input(i:i)
    if (c >= 'a' .and. c <= 'z') then
      if (c >= 'f') then
        c = char(iachar(c) - 5)
      else
        c = char(iachar(c) + 21)
      end if
    else if (c >= 'A' .and. c <= 'Z') then
      if (c >= 'F') then
        c = char(iachar(c) - 5)
      else
        c = char(iachar(c) + 21)
      end if
    end if
    result = result // c
  end do

  print *, result

end program decode_shift_demo