program decode_shift
  implicit none
  character(len=*) :: s
  character(len=len(s)) :: result
  integer :: i
  character :: c

  read(*,*) s

  do i = 1, len(s)
    c = s(i:i)
    if (c >= 'a' .and. c <= 'z') then
      result(i:i) = char(iachar(c) - 5)
    else if (c >= 'A' .and. c <= 'Z') then
      result(i:i) = char(iachar(c) - 5)
    else
      result(i:i) = c
    end if
  end do

  print *, trim(result)
end program decode_shift