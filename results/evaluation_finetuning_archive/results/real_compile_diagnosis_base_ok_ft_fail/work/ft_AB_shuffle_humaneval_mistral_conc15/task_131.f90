program digits
  implicit none
  integer :: n, result

  ! Read input
  read(*,*) n

  ! Calculate product of odd digits
  result = 0
  if (n > 0) then
    result = 1
    do while (n > 0)
      if (mod(n, 10) /= 0) then
        result = result * mod(n, 10)
      else
        result = 0
        exit
      end if
      n = n / 10
    end do
  end if

  ! Output result
  print *, result

end program digits