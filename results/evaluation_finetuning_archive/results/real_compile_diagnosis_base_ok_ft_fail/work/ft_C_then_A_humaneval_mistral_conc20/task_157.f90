program right_angle_triangle
  implicit none
  integer :: a, b, c
  logical :: result

  ! Read input values
  read(*,*) a
  read(*,*) b
  read(*,*) c

  ! Check if it's a right-angled triangle
  result = (a*a + b*b == c*c) .or. (a*a + c*c == b*b) .or. (b*b + c*c == a*a)

  ! Output result
  print *, result

end program right_angle_triangle