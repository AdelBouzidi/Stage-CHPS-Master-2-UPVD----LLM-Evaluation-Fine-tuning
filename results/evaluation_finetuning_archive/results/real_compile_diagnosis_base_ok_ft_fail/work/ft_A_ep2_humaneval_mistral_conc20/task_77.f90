program main
  implicit none
  integer :: a
  logical :: result

  ! Read input from stdin
  read(*,*) a

  ! Call the iscube function
  result = iscube(a)

  ! Output the result
  print *, 'Output: ', result
end program main