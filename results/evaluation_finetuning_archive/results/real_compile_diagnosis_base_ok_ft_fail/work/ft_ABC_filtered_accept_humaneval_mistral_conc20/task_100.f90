program make_a_pile_demo
  implicit none
  integer :: n
  integer, allocatable :: pile(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  call make_a_pile(n, pile)
  
  ! Output the result
  print *, pile
  
contains

  subroutine make_a_pile(n, pile)
    implicit none
    integer, intent(in) :: n
    integer, intent(out) :: pile(n)
    integer :: i
    
    pile(1) = n
    do i = 2, n
      pile(i) = pile(i-1) + 2
    end do
  end subroutine make_a_pile

end program make_a_pile_demo