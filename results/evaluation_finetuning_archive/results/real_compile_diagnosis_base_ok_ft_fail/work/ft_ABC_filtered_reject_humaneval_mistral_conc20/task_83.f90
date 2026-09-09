program starts_one_ends
  implicit none
  integer :: n
  integer :: result

  read *, n
  result = starts_one_ends(n)
  print *, result

end program starts_one_ends