program modp
  implicit none
  integer :: n, p, result

  ! Read input
  read(*,*) n
  read(*,*) p

  ! Compute 2^n mod p
  result = mod(2**n, p)

  ! Output result
  print *, result
end program modp