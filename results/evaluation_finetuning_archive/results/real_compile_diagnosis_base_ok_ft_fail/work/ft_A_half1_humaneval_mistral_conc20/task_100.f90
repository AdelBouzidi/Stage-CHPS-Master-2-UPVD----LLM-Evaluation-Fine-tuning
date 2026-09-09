program main
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  call make_a_pile(n, result)
  
  ! Print output
  write(*,*) result
contains

  subroutine make_a_pile(n, result)
    implicit none
    integer, intent(in) :: n
    integer, intent(out) :: result(:)
    integer :: i
    
    allocate(result(n))
    do i = 1, n
      result(i) = n + 2*(i-1)
    end do
  end subroutine make_a_pile

end program main