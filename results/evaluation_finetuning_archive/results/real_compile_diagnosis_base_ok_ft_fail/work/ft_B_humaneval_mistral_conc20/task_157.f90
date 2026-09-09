program right_angle_triangle
  implicit none
  integer :: a, b, c
  logical :: result

  read *, a
  read *, b
  read *, c

  result = (a*a + b*b == c*c) .or. (a*a + c*c == b*b) .or. (b*b + c*c == a*a)

  print *, result
end program right_angle_triangle