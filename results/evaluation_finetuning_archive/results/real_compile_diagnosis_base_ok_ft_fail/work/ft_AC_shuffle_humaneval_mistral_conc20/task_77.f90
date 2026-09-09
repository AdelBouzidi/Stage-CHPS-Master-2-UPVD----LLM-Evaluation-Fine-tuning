program iscube_demo
  implicit none
  integer :: a
  logical :: result

  ! Read input
  read *, a

  ! Call function
  result = iscube(a)

  ! Output result
  print *, result

contains

  logical function iscube(a)
    implicit none
    integer, intent(in) :: a
    integer :: root
    real :: cube

    if (a < 0) then
       root = -1
    else
       root = 0
    end if

    do while (root**3 < a)
       root = root + 1
    end do

    if (root**3 == a) then
       iscube = .true.
    else
       iscube = .false.
    end if

  end function iscube

end program iscube_demo