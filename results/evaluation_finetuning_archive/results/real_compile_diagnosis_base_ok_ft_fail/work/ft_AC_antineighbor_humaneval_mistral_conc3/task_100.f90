program main
  implicit none
  integer :: n
  integer, allocatable :: pile(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  pile = make_a_pile(n)
  
  ! Print output
  print *, pile
end program main