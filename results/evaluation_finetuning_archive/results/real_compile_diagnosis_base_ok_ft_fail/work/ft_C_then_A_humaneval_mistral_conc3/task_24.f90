program largest_divisor
  implicit none
  integer :: n, result

  ! Read input from stdin
  read(*,*) n

  ! Find largest divisor smaller than n
  result = 1
  do while (n > 1)
    if (mod(n, result + 1) == 0) then
      result = result + 1
    else
      exit
    end if
  end do

  ! Output result
  print *, result

end program largest_divisor