program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Read input
  read(*,*) a

  ! Check if a is a perfect cube
  result = iscube(a)

  ! Output result
  print *, result

contains

  function iscube(a) result(res)
    implicit none
    integer, intent(in) :: a
    logical :: res
    integer :: n
    res = .false.
    if (a >= 0) then
      n = int(a**(1.0/3.0))
      if (n**3 == a) res = .true.
    else
      n = -int((-a)**(1.0/3.0))
      if (n**3 == a) res = .true.
    end if
  end function iscube

end program iscube_demo