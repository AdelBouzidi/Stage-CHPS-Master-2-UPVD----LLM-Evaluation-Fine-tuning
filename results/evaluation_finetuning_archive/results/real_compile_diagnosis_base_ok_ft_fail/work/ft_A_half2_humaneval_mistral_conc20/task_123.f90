program main
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  read(*,*) n
  result = get_odd_collatz(n)
  print *, result
end program main