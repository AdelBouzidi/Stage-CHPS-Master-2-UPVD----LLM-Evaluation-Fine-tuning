program main
  implicit none
  integer :: n
  integer, allocatable :: pile(:)
  
  ! Read input
  read(*,*) n
  
  ! Allocate and create the pile
  allocate(pile(n))
  pile(1) = n
  do i = 2, n
    pile(i) = pile(i-1) + 2
  end do
  
  ! Output the pile
  write(*,*) (pile(i), i=1, n)
  
end program main