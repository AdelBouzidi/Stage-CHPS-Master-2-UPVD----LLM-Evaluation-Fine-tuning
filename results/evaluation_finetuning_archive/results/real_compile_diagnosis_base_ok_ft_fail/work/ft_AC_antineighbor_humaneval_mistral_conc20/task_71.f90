program triangle_area
  implicit none
  real :: a, b, c, area
  real :: s

  ! Read input values
  read(*,*) a
  read(*,*) b
  read(*,*) c

  ! Check if triangle is valid
  if (a + b > c .and. a + c > b .and. b + c > a) then
    s = (a + b + c) / 2.0
    area = sqrt(s * (s - a) * (s - b) * (s - c))
    print '(F6.2)', area
  else
    print *, -1.0
  end if

end program triangle_area