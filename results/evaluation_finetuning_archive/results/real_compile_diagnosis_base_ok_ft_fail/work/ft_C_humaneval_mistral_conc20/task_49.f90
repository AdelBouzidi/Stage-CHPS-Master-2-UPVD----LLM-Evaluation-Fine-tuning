program modp
  implicit none
  integer :: n, p, result

  read(*,*) n, p
  result = 2**n
  result = mod(result, p)
  print *, result
end program modp