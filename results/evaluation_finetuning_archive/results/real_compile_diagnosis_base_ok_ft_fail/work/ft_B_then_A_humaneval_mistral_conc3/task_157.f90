program right_angle_triangle_prog
  implicit none
  integer :: a, b, c
  logical :: res

  read *, a, b, c
  res = right_angle_triangle ( a, b, c )
  print *, res

contains

  logical function right_angle_triangle ( integer a, integer b, integer c )
    implicit none
    if ( a*a + b*b == c*c .or. a*a + c*c == b*b .or. b*b + c*c == a*a ) then
       right_angle_triangle = .true.
    else
       right_angle_triangle = .false.
    end if
  end function right_angle_triangle

end program right_angle_triangle_prog