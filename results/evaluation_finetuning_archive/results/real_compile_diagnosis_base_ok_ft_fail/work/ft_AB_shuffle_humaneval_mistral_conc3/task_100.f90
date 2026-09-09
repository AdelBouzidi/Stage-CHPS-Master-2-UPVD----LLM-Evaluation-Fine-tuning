program make_a_pile
  implicit none
  integer :: n
  integer, allocatable :: pile(:)
  
  ! Read input
  read(*,*) n
  
  ! Allocate array
  allocate(pile(n))
  
  ! Initialize first element
  pile(1) = n
  
  ! Fill remaining elements
  do i = 2, n
    pile(i) = pile(i-1) + 2
  end do
  
  ! Output result
  write(*,*) pile
  
end program make_a_pile