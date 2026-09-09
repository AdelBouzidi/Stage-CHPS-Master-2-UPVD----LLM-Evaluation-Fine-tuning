program make_a_pile
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read *, n
  
  ! Create the pile
  allocate(result(n))
  result = [ (n + 2*(i-1), i = 1, n) ]
  
  ! Output the result
  print *, result
  
end program make_a_pile