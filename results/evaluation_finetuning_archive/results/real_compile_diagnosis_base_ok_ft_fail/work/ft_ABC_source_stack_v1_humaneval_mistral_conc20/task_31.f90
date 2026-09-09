program main
  implicit none
  integer :: n
  logical :: result

  read *, n
  result = is_prime(n)
  print *, result
end program main