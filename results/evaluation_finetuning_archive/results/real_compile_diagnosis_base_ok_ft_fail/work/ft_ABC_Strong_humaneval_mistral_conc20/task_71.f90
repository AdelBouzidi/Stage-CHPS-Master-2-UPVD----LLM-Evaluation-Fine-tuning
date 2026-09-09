program triangle_area_demo
  implicit none
  real :: a, b, c, area
  real :: s

  ! Read input values
  read(*,*) a
  read(*,*) b
  read(*,*) c

  ! Check if triangle is valid
  if (a + b > c .and. a + c > b .and. b + c > a) then
    ! Calculate area using Heron's formula
    s = (a + b + c) / 2.0
    area = sqrt(s * (s - a) * (s - b) * (s - c))
    print(*,'(F6.2)') area
  else
    print(*,'(I6)') -1
  end if

end program triangle_area_demo