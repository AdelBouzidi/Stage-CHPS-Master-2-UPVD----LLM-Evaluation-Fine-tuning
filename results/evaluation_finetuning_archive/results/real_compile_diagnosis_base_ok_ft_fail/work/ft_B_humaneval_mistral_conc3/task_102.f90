program choose_num
  implicit none
  integer :: x, y, result

  read *, x
  read *, y

  if (x > y) then
    result = -1
  else if (mod(y, 2) == 0) then
    result = y
  else
    result = y - 1
  end if

  write *, result

end program choose_num