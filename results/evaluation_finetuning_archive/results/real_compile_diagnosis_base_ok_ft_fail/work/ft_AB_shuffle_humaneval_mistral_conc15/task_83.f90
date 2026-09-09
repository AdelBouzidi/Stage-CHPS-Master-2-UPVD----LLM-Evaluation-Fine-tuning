program starts_one_ends
  implicit none
  integer :: n
  integer :: result

  ! Read input from stdin
  read(*,*) n

  ! Calculate result
  if (n == 1) then
    result = 1
  else
    result = 17 * 10**(n-1)
  end if

  ! Output result
  print *, result

end program starts_one_ends