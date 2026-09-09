program triangle_area
  implicit none
  real :: base, height, area

  read *, base
  read *, height
  area = 0.5 * base * height
  print *, area
end program triangle_area