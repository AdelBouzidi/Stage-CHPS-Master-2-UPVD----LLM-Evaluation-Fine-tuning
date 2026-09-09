program main
  implicit none
  integer :: n
  integer, allocatable :: factors(:)
  
  ! Read input
  read(*,*) n
  
  ! Call factorize
  call factorize(n, factors)
  
  ! Output result
  write(*,*) factors
end program main