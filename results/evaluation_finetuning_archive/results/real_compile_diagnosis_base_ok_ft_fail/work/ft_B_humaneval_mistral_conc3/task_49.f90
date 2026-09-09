program modp
  implicit none
  integer :: n, p, result

  read *, n
  read *, p

  result = 2**n
  result = mod(result, p)

  write *, result

end program modp