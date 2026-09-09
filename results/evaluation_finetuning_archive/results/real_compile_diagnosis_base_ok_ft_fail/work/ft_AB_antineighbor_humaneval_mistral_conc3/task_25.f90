program factorize_demo
  implicit none
  integer :: n
  integer, allocatable :: factors(:)
  
  ! Read input
  read(*,*) n
  
  ! Call factorize function
  factors = factorize(n)
  
  ! Output results
  print *, factors
end program factorize_demo