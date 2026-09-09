program triangle_area
  implicit none
  real :: a, h, area

  ! Read input values
  read(*,*) a
  read(*,*) h

  ! Compute area of triangle
  area = 0.5 * a * h

  ! Output result
  print(*,'(F6.1)') area

end program triangle_area