program largest_divisor
  implicit none
  integer :: n, result

  ! Read input
  read(*,*) n

  ! Find largest divisor smaller than n
  result = 1
  do while (result * 2 <= n)
    if (mod(n, result * 2) == 0) then
      result = result * 2
    else
      result = result + 1
    end if
  end do

  ! Output result
  print *, result

end program largest_divisor