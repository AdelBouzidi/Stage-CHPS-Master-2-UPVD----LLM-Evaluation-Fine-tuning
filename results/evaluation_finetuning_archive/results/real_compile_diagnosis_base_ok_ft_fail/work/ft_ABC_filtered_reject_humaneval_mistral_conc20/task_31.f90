program main
  implicit none
  integer :: n
  logical :: result

  ! Read input
  read(*,*) n

  ! Call the function
  result = is_prime(n)

  ! Output result
  print *, result
end program main