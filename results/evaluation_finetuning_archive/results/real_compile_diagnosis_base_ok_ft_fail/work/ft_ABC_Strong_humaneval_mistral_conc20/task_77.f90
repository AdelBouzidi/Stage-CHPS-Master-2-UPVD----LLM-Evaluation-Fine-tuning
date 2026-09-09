program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Read input
  read(*,*) a

  ! Call the function
  result = iscube(a)

  ! Print output
  print *, result

contains

  logical function iscube(a)
    integer, intent(in) :: a
    integer :: root
    root = int(a**(1.0/3.0))
    if (root**3 == a) then
      iscube = .true.
    else
      iscube = .false.
    end if
  end function iscube

end program iscube_demo