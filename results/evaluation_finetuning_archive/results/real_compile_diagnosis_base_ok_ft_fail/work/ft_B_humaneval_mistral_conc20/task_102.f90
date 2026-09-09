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
    if (y - 1 >= x) then
      result = y - 1
    else
      result = -1
    end if
  end if

  write *, result

end program choose_num