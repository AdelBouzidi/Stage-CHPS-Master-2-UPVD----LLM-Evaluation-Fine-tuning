program digits
  implicit none
  integer :: n, result
  integer :: digit, product

  read(*,*) n

  result = 0
  product = 1
  do while (n > 0)
    digit = mod(n, 10)
    if (mod(digit, 2) == 1) then
      product = product * digit
    end if
    n = n / 10
  end do

  if (product == 1) then
    result = 0
  else
    result = product
  end if

  write(*,*) result

end program digits