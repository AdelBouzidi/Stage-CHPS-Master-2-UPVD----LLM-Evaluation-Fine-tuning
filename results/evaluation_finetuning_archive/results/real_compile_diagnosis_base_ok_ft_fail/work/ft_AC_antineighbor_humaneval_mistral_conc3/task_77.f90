program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Read input
  read *, a

  ! Call function
  result = iscube(a)

  ! Print output
  print *, result

contains

  logical function iscube(a)
    implicit none
    integer, intent(in) :: a
    integer :: root
    real :: cube

    if (a == 0) then
       iscube = .true.
    else
       root = nint(abs(a)**(1.0/3.0))
       if (cube * root**3 == abs(a)) then
          iscube = .true.
       else
          iscube = .false.
       end if
    end if
  end function iscube

end program iscube_demo