program digits
  implicit none
  integer :: n, result, digit, product

  read(*,*) n

  result = 0
  product = 1
  do while (n > 0)
    digit = mod(n, 10)
    if (mod(digit, 2) == 1) then
      product = product * digit
    else
      result = 0
    end if
    n = n / 10
  end do

  if (result == 0) then
    print *, 0
  else
    print *, product
  end if

end program digits