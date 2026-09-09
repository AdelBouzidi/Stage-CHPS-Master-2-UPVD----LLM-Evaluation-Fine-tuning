program triangle_area_demo
  implicit none
  real :: base, height, area

  ! Read base and height from input
  read(*,*) base
  read(*,*) height

  ! Compute area
  area = 0.5 * base * height

  ! Print result
  print *, area

end program triangle_area_demo