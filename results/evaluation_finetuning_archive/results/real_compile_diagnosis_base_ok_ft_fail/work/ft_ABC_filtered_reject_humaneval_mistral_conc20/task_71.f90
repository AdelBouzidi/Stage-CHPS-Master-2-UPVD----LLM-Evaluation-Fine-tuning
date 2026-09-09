program triangle_area
  implicit none
  real :: a, b, c, area
  integer :: result

  ! Read input
  read(*,*) a
  read(*,*) b
  read(*,*) c

  ! Calculate area using Heron's formula
  result = triangle_area(a, b, c)

  ! Output result
  if (result < 0) then
    write(*,*) -1.00
  else
    write(*,*) result
  end if

contains

  function triangle_area(a, b, c) result(area)
    implicit none
    real, intent(in) :: a, b, c
    real :: area
    real :: s

    ! Check if triangle is valid
    if (a + b <= c .or. a + c <= b .or. b + c <= a) then
      area = -1.0
    else
      s = (a + b + c) / 2.0
      area = sqrt(s * (s - a) * (s - b) * (s - c))
    end if
  end function triangle_area

end program triangle_area