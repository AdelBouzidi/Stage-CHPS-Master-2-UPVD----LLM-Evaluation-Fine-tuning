program main
  implicit none
  integer :: n
  logical :: result

  ! Read input from stdin
  read(*,*) n

  ! Call the is_prime function
  result = is_prime(n)

  ! Output the result
  print *, result
end program main