program main
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  read(*,*) n
  result = f(n)
  print *, result
end program main