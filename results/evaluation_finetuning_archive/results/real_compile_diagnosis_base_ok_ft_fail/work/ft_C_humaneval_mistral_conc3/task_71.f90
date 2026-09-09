program triangle_area
  implicit none
  real :: a, b, c, area
  real :: s

  ! Read the three sides
  read(*,*) a
  read(*,*) b
  read(*,*) c

  ! Check if triangle is valid (triangle inequality)
  if (a + b > c .and. a + c > b .and. b + c > a) then
    ! Calculate semi-perimeter
    s = (a + b + c) / 2.0
    ! Calculate area using Heron's formula
    area = sqrt(s * (s - a) * (s - b) * (s - c))
    ! Output rounded to 2 decimal places
    print*, trim(adjustl(format(f6.2, area)))
  else
    print*, -1.0
  end if

end program triangle_area