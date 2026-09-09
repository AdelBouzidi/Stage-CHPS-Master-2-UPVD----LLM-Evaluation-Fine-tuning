program largest_divisor
  implicit none
  integer :: n, result

  ! Read input
  read(*,*) n

  ! Find largest divisor smaller than n
  result = 1
  do i = n/2, 1, -1
    if (mod(n, i) == 0) then
      result = i
      exit
    end if
  end do

  ! Output result
  print *, result

end program largest_divisor