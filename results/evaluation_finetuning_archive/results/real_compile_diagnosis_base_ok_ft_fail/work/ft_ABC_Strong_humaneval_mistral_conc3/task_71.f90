program triangle_area_demo
  implicit none
  real :: a, b, c, area
  logical :: valid

  ! Read input values
  read(*,*) a
  read(*,*) b
  read(*,*) c

  ! Check if triangle is valid (triangle inequality)
  valid = (a + b > c) .and. (a + c > b) .and. (b + c > a)

  if (valid) then
    ! Calculate semi-perimeter
    real :: s
    s = (a + b + c) / 2.0
    ! Calculate area using Heron's formula
    area = sqrt(s * (s - a) * (s - b) * (s - c))
    print *, area
  else
    print *, -1.0
  end if

end program triangle_area_demo