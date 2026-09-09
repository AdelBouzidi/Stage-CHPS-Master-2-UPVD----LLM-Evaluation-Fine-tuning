program triangle_area_demo
  implicit none
  integer, parameter :: sp = kind(1.0)
  real(sp) :: a, b, c, area

  read(*,*) a
  read(*,*) b
  read(*,*) c
  area = triangle_area(a, b, c)
  print *, area

contains

  function triangle_area(a, b, c) result(area)
    implicit none
    real(sp), intent(in) :: a, b, c
    real(sp) :: area
    real(sp) :: s
    
    if (a <= 0.0_sp .or. b <= 0.0_sp .or. c <= 0.0_sp .or. &
        a + b <= c .or. a + c <= b .or. b + c <= a) then
      area = -1.0_sp
    else
      s = (a + b + c) / 2.0_sp
      area = sqrt(s * (s - a) * (s - b) * (s - c))
    end if
  end function triangle_area

end program triangle_area_demo