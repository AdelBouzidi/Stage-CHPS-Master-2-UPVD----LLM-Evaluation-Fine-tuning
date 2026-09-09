program triangle_area_demo
  implicit none
  real :: a, b, c, area
  logical :: valid

  ! Read input
  read(*,*) a
  read(*,*) b
  read(*,*) c

  ! Check if triangle is valid
  if (a + b > c .and. a + c > b .and. b + c > a) then
    valid = .true.
    area = sqrt((a + b + c) / 2.0 * ((a + b + c) / 2.0 - a) * ((a + b + c) / 2.0 - b) * ((a + b + c) / 2.0 - c))
    print '(F6.2)', area
  else
    valid = .false.
    print '(F6.2)', -1.0
  end if

end program triangle_area_demo