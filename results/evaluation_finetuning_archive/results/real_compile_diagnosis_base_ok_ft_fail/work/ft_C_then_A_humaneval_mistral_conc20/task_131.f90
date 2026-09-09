program digits
  implicit none
  integer :: n, result
  integer :: i, digit, product

  ! Read input
  read(*,*) n

  ! Calculate product of odd digits
  product = 1
  do i = 1, n
    digit = mod(i, 10)
    if (mod(digit, 2) == 1) then
      product = product * digit
    else
      product = 0
      exit
    end if
  end do

  ! Output result
  print *, product

end program digits