program triangle_area
  implicit none
  real :: a, h, area
  read(*,*) a, h
  area = 0.5 * a * h
  print *, area
end program triangle_area