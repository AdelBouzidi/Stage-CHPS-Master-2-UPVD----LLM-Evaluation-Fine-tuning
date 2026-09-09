program starts_one_ends
  implicit none
  integer :: n, result

  read *, n

  if (n == 1) then
    result = 1
  else
    result = 10**(n-1) + 8*10**(n-2)
  end if

  write *, result

end program starts_one_ends