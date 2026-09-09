program main
  implicit none
  integer :: n
  integer, allocatable :: pile(:)
  
  ! Read input
  read *, n
  
  ! Create the pile
  allocate(pile(n))
  pile(1) = n
  do i = 2, n
    pile(i) = pile(i-1) + 2
  end do
  
  ! Output the result
  print *, pile
  
end program main