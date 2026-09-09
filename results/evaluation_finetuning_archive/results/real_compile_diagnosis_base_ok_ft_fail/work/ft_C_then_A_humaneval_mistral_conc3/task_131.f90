program digits
  implicit none
  integer :: n, result
  integer :: i, digit

  ! Read input
  read(*,*) n

  ! Calculate product of odd digits
  result = 1
  do i = 1, n
    digit = mod(i, 10)
    if (digit /= 0 .and. digit /= 2 .and. digit /= 4 .and. digit /= 6 .and. digit /= 8) then
      result = result * digit
    end if
  end do

  ! Output result
  print *, result

end program digits