program starts_one_ends
  implicit none
  integer :: n
  integer :: result

  ! Read input from stdin
  read(*,*) n

  ! Compute result
  if (n <= 0) then
    result = 0
  else if (n == 1) then
    result = 1
  else
    result = 2 * 10**(n-1) - 10**(n-2)
  end if

  ! Output result
  print *, result

end program starts_one_ends