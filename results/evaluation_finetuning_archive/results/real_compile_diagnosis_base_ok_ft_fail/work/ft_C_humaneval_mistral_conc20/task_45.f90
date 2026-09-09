program triangle_area
  implicit none
  real :: base, height, area

  ! Read base and height from input
  read(*,*) base
  read(*,*) height

  ! Compute area
  area = 0.5 * base * height

  ! Output the result
  print*, area
end program triangle_area