program main
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  result = make_a_pile(n)
  
  ! Output the result
  print *, result
end program main