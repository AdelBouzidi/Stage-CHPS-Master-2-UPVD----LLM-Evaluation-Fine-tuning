program main
  implicit none
  integer :: a
  logical :: result
  
  ! Read input
  read *, a
  
  ! Call the function
  result = iscube(a)
  
  ! Print output
  print *, result
end program main