program digits
  implicit none
  integer :: n, result
  integer :: digit, product
  logical :: all_even

  ! Read input
  read(*,*) n

  ! Initialize variables
  product = 1
  all_even = .true.

  ! Process each digit
  do while (n > 0)
    digit = mod(n, 10)
    if (mod(digit, 2) == 1) then
      product = product * digit
      all_even = .false.
    else
      all_even = .true.
    end if
    n = n / 10
  end do

  ! Output result
  if (all_even) then
    result = 0
  else
    result = product
  end if

  print *, result

end program digits