program main
  implicit none
  integer :: n
  integer, allocatable :: pile(:)
  
  ! Read input
  read(*,*) n
  
  ! Create pile array
  allocate(pile(n))
  pile(1) = n
  if (mod(n, 2) == 1) then
    pile(2) = n + 2
    do i = 3, n
      pile(i) = pile(i-1) + 2
    end do
  else
    pile(2) = n + 2
    do i = 3, n
      pile(i) = pile(i-1) + 2
    end do
  end if
  
  ! Print output
  print *, pile
end program main