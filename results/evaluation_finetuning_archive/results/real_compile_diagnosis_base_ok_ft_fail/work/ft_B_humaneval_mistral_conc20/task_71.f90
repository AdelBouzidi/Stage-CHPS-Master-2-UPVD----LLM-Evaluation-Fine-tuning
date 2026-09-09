program triangle_area
  implicit none
  real :: a, b, c, s, area
  real :: result

  ! Read the three sides
  read *, a
  read *, b
  read *, c

  ! Check if triangle is valid (triangle inequality)
  if (a + b > c .and. a + c > b .and. b + c > a) then
    ! Calculate semi-perimeter
    s = (a + b + c) / 2.0
    ! Calculate area using Heron's formula
    area = sqrt(s * (s - a) * (s - b) * (s - c))
    ! Output area rounded to 2 decimal places
    result = area
  else
    result = -1.0
  end if

  ! Output the result
  write (*, '(F10.2)') result

end program triangle_area