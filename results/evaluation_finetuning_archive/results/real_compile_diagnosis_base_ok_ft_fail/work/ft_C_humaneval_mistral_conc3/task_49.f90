program modp
  implicit none
  integer :: n, p, result, i

  ! Read input
  read(*,*) n, p

  ! Compute 2^n mod p
  result = 1
  do i = 1, n
    result = (result * 2) mod p
  end do

  ! Print output
  print *, result
end program modp